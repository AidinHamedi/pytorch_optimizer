import math

import torch
from torch.optim.optimizer import Optimizer

from pytorch_optimizer.base.exception import NoSparseGradientError, ZeroParameterSizeError
from pytorch_optimizer.base.optimizer import BaseOptimizer
from pytorch_optimizer.base.types import BETAS, CLOSURE, DEFAULTS, LOSS, PARAMETERS


class AdamS(Optimizer, BaseOptimizer):
    r"""Adam with stable weight decay.

    :param params: PARAMETERS. iterable of parameters to optimize or dicts defining parameter groups.
    :param lr: float. learning rate.
    :param betas: BETAS. coefficients used for computing running averages of gradient and the squared hessian trace.
    :param weight_decay: float. weight decay (L2 penalty).
    :param ams_bound: bool. whether to use the AMSBound variant.
    :param r: float. EMA factor. between 0.9 ~ 0.99 is preferred.
    :param adanorm: bool. whether to use the AdaNorm variant.
    :param adam_debias: bool. Only correct the denominator to avoid inflating step sizes early in training.
    :param eps: float. term added to the denominator to improve numerical stability.
    """

    def __init__(
        self,
        params: PARAMETERS,
        lr: float = 1e-3,
        betas: BETAS = (0.9, 0.999),
        weight_decay: float = 1e-4,
        ams_bound: bool = False,
        r: float = 0.95,
        adanorm: bool = False,
        adam_debias: bool = False,
        eps: float = 1e-8,
    ):
        self.lr = lr
        self.betas = betas
        self.weight_decay = weight_decay
        self.eps = eps

        self.validate_parameters()

        defaults: DEFAULTS = {
            'lr': lr,
            'betas': betas,
            'weight_decay': weight_decay,
            'ams_bound': ams_bound,
            'adanorm': adanorm,
            'adam_debias': adam_debias,
            'eps': eps,
        }
        if adanorm:
            defaults.update({'r': r})

        super().__init__(params, defaults)

    def validate_parameters(self):
        self.validate_learning_rate(self.lr)
        self.validate_betas(self.betas)
        self.validate_weight_decay(self.weight_decay)
        self.validate_epsilon(self.eps)

    def __str__(self) -> str:
        return 'AdamS'

    @torch.no_grad()
    def reset(self):
        for group in self.param_groups:
            for p in group['params']:
                state = self.state[p]

                state['step'] = 0
                state['exp_avg'] = torch.zeros_like(p)
                state['exp_avg_sq'] = torch.zeros_like(p)
                if group['ams_bound']:
                    state['max_exp_avg_sq'] = torch.zeros_like(p)
                if group['adanorm']:
                    state['exp_grad_norm'] = torch.zeros((1,), dtype=p.dtype, device=p.device)

    @torch.no_grad()
    def step(self, closure: CLOSURE = None) -> LOSS:
        loss: LOSS = None
        if closure is not None:
            with torch.enable_grad():
                loss = closure()

        param_size: int = 0
        exp_avg_sq_hat_sum: float = 0.0

        for group in self.param_groups:
            beta1, beta2 = group['betas']
            for p in group['params']:
                if p.grad is None:
                    continue

                grad = p.grad
                if grad.is_sparse:
                    raise NoSparseGradientError(str(self))

                param_size += p.numel()

                state = self.state[p]

                if len(state) == 0:
                    state['step'] = 0
                    state['exp_avg'] = torch.zeros_like(p)
                    state['exp_avg_sq'] = torch.zeros_like(p)
                    if group['ams_bound']:
                        state['max_exp_avg_sq'] = torch.zeros_like(p)
                    if group['adanorm']:
                        state['exp_grad_norm'] = torch.zeros((1,), dtype=p.dtype, device=p.device)

                state['step'] += 1

                bias_correction2: float = 1.0 - beta2 ** state['step']

                s_grad = self.get_adanorm_gradient(
                    grad=grad,
                    adanorm=group['adanorm'],
                    exp_grad_norm=state.get('exp_grad_norm', None),
                    r=group.get('r', None),
                )

                exp_avg, exp_avg_sq = state['exp_avg'], state['exp_avg_sq']
                exp_avg.mul_(beta1).add_(s_grad, alpha=1.0 - beta1)
                exp_avg_sq.mul_(beta2).addcmul_(grad, grad, value=1.0 - beta2)

                if group['ams_bound']:
                    max_exp_avg_sq = state['max_exp_avg_sq']
                    torch.max(max_exp_avg_sq, exp_avg_sq, out=max_exp_avg_sq)
                    exp_avg_sq_hat = max_exp_avg_sq
                else:
                    exp_avg_sq_hat = exp_avg_sq

                exp_avg_sq_hat_sum += exp_avg_sq_hat.sum() / bias_correction2

        if param_size == 0:
            raise ZeroParameterSizeError()

        exp_avg_sq_hat_mean: float = math.sqrt(exp_avg_sq_hat_sum / param_size)

        for group in self.param_groups:
            beta1, beta2 = group['betas']
            for p in group['params']:
                if p.grad is None:
                    continue

                state = self.state[p]

                if group['weight_decay'] > 0.0:
                    p.mul_(1.0 - group['lr'] * group['weight_decay'] / (exp_avg_sq_hat_mean + group['eps']))

                bias_correction1 = 1.0 - beta1 ** state['step']
                bias_correction2 = 1.0 - beta2 ** state['step']

                exp_avg_sq_hat = state['max_exp_avg_sq'] if group['ams_bound'] else state['exp_avg_sq']
                exp_avg_sq_hat.div_(bias_correction2)

                de_nom = exp_avg_sq_hat.sqrt().add(group['eps'])

                step_size = group['lr'] if group['adam_debias'] else group['lr'] / bias_correction1
                p.addcdiv_(state['exp_avg'], de_nom, value=-step_size)

        return loss

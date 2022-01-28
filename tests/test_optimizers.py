from typing import Callable, Dict, List, Tuple

import numpy as np
import pytest
import torch
from torch import nn
from torch.optim import Optimizer

from pytorch_optimizer import (
    MADGRAD,
    SGDP,
    AdaBelief,
    AdaBound,
    AdaHessian,
    AdamP,
    DiffGrad,
    DiffRGrad,
    Lamb,
    Lookahead,
    RAdam,
    Ranger,
)

__REFERENCE__ = 'https://github.com/jettify/pytorch-optimizer/blob/master/tests/test_optimizer_with_nn.py'


class LogisticRegression(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(2, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.fc1(x)


def make_dataset(num_samples: int = 100, dims: int = 2, seed: int = 42) -> Tuple[torch.Tensor, torch.Tensor]:
    rng = np.random.RandomState(seed)

    x = rng.randn(num_samples, dims) * 2

    # center the first N/2 points at (-2, -2)
    mid: int = num_samples // 2
    x[:mid, :] = x[:mid, :] - 2 * np.ones((mid, dims))

    # center the last N/2 points at (2, 2)
    x[mid:, :] = x[mid:, :] + 2 * np.ones((mid, dims))

    # labels: first N/2 are 0, last N/2 are 1
    y = np.array([0] * mid + [1] * mid).reshape(100, 1)

    x = torch.Tensor(x)
    y = torch.Tensor(y)

    return x, y


def ids(v) -> str:
    return f'{v[0].__name__}_{v[1:]}'


def build_lookahead(*a, **kwargs):
    return Lookahead(AdamP(*a, **kwargs))


optimizers: List[Tuple[Optimizer, Dict[str, float]], int] = [
    (build_lookahead, {'lr': 0.1, 'weight_decay': 1e-3}, 200),
    (AdaBelief, {'lr': 0.1, 'weight_decay': 1e-3}, 200),
    (AdaBound, {'lr': 1.5, 'gamma': 0.1, 'weight_decay': 1e-3}, 200),
    (AdamP, {'lr': 0.045, 'weight_decay': 1e-3}, 800),
    (DiffGrad, {'lr': 0.5, 'weight_decay': 1e-3}, 200),
    (DiffRGrad, {'lr': 0.5, 'weight_decay': 1e-3}, 200),
    (Lamb, {'lr': 0.0151, 'weight_decay': 1e-3}, 1000),
    (MADGRAD, {'lr': 1.0, 'weight_decay': 1e-3}, 200),
    (RAdam, {'lr': 1.0, 'weight_decay': 1e-3}, 200),
    (Ranger, {'lr': 0.1, 'weight_decay': 1e-3}, 200),
    (SGDP, {'lr': 1.0, 'weight_decay': 1e-3}, 200),
    (AdaHessian, {'lr': 0.1, 'weight_decay': 1e-3}, 200),
]


@pytest.mark.parametrize('optimizer_config', optimizers, ids=ids)
def test_optimizers(optimizer_config):
    torch.manual_seed(42)

    x_data, y_data = make_dataset()

    model: nn.Module = LogisticRegression()
    loss_fn: nn.Module = nn.BCEWithLogitsLoss()

    optimizer_class, config, iterations = optimizer_config
    optimizer = optimizer_class(model.parameters(), **config)

    loss: float = np.inf
    init_loss: float = np.inf
    for _ in range(iterations):
        optimizer.zero_grad()

        y_pred = model(x_data)
        loss = loss_fn(y_pred, y_data)

        if init_loss == np.inf:
            init_loss = loss

        loss.backward(create_graph=True)

        optimizer.step()

    assert init_loss > 2.0 * loss

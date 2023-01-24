from typing import Any, Dict, List, Tuple, Union

from pytorch_optimizer import (
    LARS,
    MADGRAD,
    PNM,
    SGDP,
    AdaBelief,
    AdaBound,
    Adai,
    AdamP,
    Adan,
    AdaPNM,
    DiffGrad,
    DiffRGrad,
    Lamb,
    Nero,
    RAdam,
    RaLamb,
    Ranger,
    Ranger21,
    Shampoo,
)
from tests.utils import build_lookahead

ADAPTIVE_FLAGS: List[bool] = [True, False]
PULLBACK_MOMENTUM: List[str] = ['none', 'reset', 'pullback']

SPARSE_OPTIMIZERS: List[str] = [
    'madgrad',
]
NO_SPARSE_OPTIMIZERS: List[str] = [
    'adamp',
    'sgdp',
    'madgrad',
    'ranger',
    'ranger21',
    'radam',
    'adabound',
    'adabelief',
    'diffgrad',
    'diffrgrad',
    'lamb',
    'ralamb',
    'lars',
    'shampoo',
    'nero',
    'adan',
    'adai',
    'adapnm',
    'pnm',
]
VALID_OPTIMIZER_NAMES: List[str] = [
    'adamp',
    'adan',
    'sgdp',
    'madgrad',
    'ranger',
    'ranger21',
    'radam',
    'adabound',
    'adabelief',
    'diffgrad',
    'diffrgrad',
    'lamb',
    'ralamb',
    'lars',
    'shampoo',
    'pnm',
    'adapnm',
    'nero',
    'adai',
]
INVALID_OPTIMIZER_NAMES: List[str] = [
    'asam',
    'sam',
    'gsam',
    'pcgrad',
    'adamd',
    'lookahead',
    'chebyshev_schedule',
]
BETA_OPTIMIZER_NAMES: List[str] = [
    'adabelief',
    'adabound',
    'adamp',
    'diffgrad',
    'diffrgrad',
    'lamb',
    'radam',
    'ranger',
    'ranger21',
    'ralamb',
    'pnm',
    'adapnm',
    'adan',
    'adai',
]

VALID_LR_SCHEDULER_NAMES: List[str] = [
    'CosineAnnealingWarmupRestarts',
    'ConstantLR',
    'CosineAnnealingLR',
    'CosineAnnealingWarmRestarts',
    'CyclicLR',
    'OneCycleLR',
]
INVALID_LR_SCHEDULER_NAMES: List[str] = [
    'dummy',
]

OPTIMIZERS: List[Tuple[Any, Dict[str, Union[float, bool, int]], int]] = [
    (build_lookahead, {'lr': 5e-1, 'weight_decay': 1e-3}, 10),
    (AdaBelief, {'lr': 5e-1, 'weight_decay': 1e-3}, 10),
    (AdaBelief, {'lr': 5e-1, 'weight_decay': 1e-3, 'amsgrad': True}, 10),
    (AdaBelief, {'lr': 5e-1, 'weight_decay': 1e-3, 'weight_decouple': False}, 10),
    (AdaBelief, {'lr': 5e-1, 'weight_decay': 1e-3, 'fixed_decay': True}, 10),
    (AdaBelief, {'lr': 5e-1, 'weight_decay': 1e-3, 'rectify': False}, 10),
    (AdaBound, {'lr': 5e-1, 'gamma': 0.1, 'weight_decay': 1e-3}, 100),
    (AdaBound, {'lr': 5e-1, 'gamma': 0.1, 'weight_decay': 1e-3, 'fixed_decay': True}, 100),
    (AdaBound, {'lr': 5e-1, 'gamma': 0.1, 'weight_decay': 1e-3, 'weight_decouple': False}, 100),
    (AdaBound, {'lr': 5e-1, 'gamma': 0.1, 'weight_decay': 1e-3, 'amsbound': True}, 100),
    (Adai, {'lr': 1e-1, 'weight_decay': 0.0}, 200),
    (Adai, {'lr': 1e-1, 'weight_decay': 0.0, 'use_gc': True}, 200),
    (Adai, {'lr': 1e-1, 'weight_decay': 0.0, 'dampening': 0.9}, 200),
    (Adai, {'lr': 1e-1, 'weight_decay': 1e-4, 'weight_decouple': False}, 200),
    (Adai, {'lr': 1e-1, 'weight_decay': 1e-4, 'weight_decouple': True}, 200),
    (AdamP, {'lr': 5e-1, 'weight_decay': 1e-3}, 10),
    (AdamP, {'lr': 5e-1, 'weight_decay': 1e-3, 'use_gc': True}, 10),
    (AdamP, {'lr': 5e-1, 'weight_decay': 1e-3, 'nesterov': True}, 10),
    (DiffGrad, {'lr': 5e-1, 'weight_decay': 1e-3}, 10),
    (DiffRGrad, {'lr': 5e-1, 'weight_decay': 1e-3}, 100),
    (Lamb, {'lr': 1e-1, 'weight_decay': 1e-3}, 50),
    (Lamb, {'lr': 1e-1, 'weight_decay': 1e-3, 'adam': True, 'eps': 1e-8}, 50),
    (Lamb, {'lr': 1e-1, 'weight_decay': 1e-3, 'pre_norm': True, 'eps': 1e-8}, 500),
    (LARS, {'lr': 1e-1, 'weight_decay': 1e-3}, 300),
    (RaLamb, {'lr': 1e-1, 'weight_decay': 1e-4}, 100),
    (RaLamb, {'lr': 1e-2, 'weight_decay': 1e-4, 'pre_norm': True}, 100),
    (RaLamb, {'lr': 1e-2, 'weight_decay': 1e-4, 'degenerated_to_sgd': True}, 100),
    (MADGRAD, {'lr': 1e-2, 'weight_decay': 1e-3}, 100),
    (MADGRAD, {'lr': 1e-2, 'weight_decay': 1e-3, 'eps': 0.0}, 100),
    (MADGRAD, {'lr': 1e-2, 'weight_decay': 1e-3, 'momentum': 0.0}, 100),
    (MADGRAD, {'lr': 1e-2, 'weight_decay': 1e-3, 'decouple_decay': True}, 100),
    (RAdam, {'lr': 1e-1, 'weight_decay': 1e-3}, 200),
    (RAdam, {'lr': 1e-1, 'weight_decay': 1e-3, 'degenerated_to_sgd': True}, 200),
    (SGDP, {'lr': 5e-2, 'weight_decay': 1e-4}, 100),
    (SGDP, {'lr': 5e-2, 'weight_decay': 1e-4, 'nesterov': True}, 100),
    (Ranger, {'lr': 5e-1, 'weight_decay': 1e-3}, 200),
    (Ranger21, {'lr': 5e-1, 'weight_decay': 1e-3, 'num_iterations': 500}, 200),
    (Shampoo, {'lr': 5e-2, 'weight_decay': 1e-3, 'momentum': 0.01}, 300),
    (PNM, {'lr': 3e-1}, 50),
    (PNM, {'lr': 3e-1, 'weight_decouple': False}, 50),
    (AdaPNM, {'lr': 3e-1, 'weight_decay': 1e-3}, 50),
    (AdaPNM, {'lr': 3e-1, 'weight_decay': 1e-3, 'weight_decouple': False}, 50),
    (AdaPNM, {'lr': 3e-1, 'weight_decay': 1e-3, 'amsgrad': False}, 50),
    (Nero, {'lr': 5e-1}, 100),
    (Nero, {'lr': 5e-1, 'constraints': False}, 100),
    (Adan, {'lr': 5e-1}, 100),
    (Adan, {'lr': 1e-0, 'weight_decay': 1e-3, 'use_gc': True}, 100),
    (Adan, {'lr': 1e-0, 'weight_decay': 1e-3, 'use_gc': True, 'weight_decouple': True}, 100),
]
ADAMD_SUPPORTED_OPTIMIZERS: List[Tuple[Any, Dict[str, Union[float, bool, int]], int]] = [
    (build_lookahead, {'lr': 5e-1, 'weight_decay': 1e-3, 'adamd_debias_term': True}, 10),
    (AdaBelief, {'lr': 5e-1, 'weight_decay': 1e-3, 'adamd_debias_term': True}, 50),
    (AdaBound, {'lr': 5e-1, 'gamma': 0.1, 'weight_decay': 1e-3, 'adamd_debias_term': True}, 100),
    (AdaBound, {'lr': 1e-2, 'gamma': 0.1, 'weight_decay': 1e-3, 'amsbound': True, 'adamd_debias_term': True}, 100),
    (AdamP, {'lr': 5e-1, 'weight_decay': 1e-3, 'adamd_debias_term': True}, 10),
    (DiffGrad, {'lr': 5e-1, 'weight_decay': 1e-3, 'adamd_debias_term': True}, 10),
    (DiffRGrad, {'lr': 1e-1, 'weight_decay': 1e-3, 'adamd_debias_term': True}, 100),
    (Lamb, {'lr': 1e-1, 'weight_decay': 1e-3, 'adamd_debias_term': True}, 50),
    (RaLamb, {'lr': 1e-1, 'weight_decay': 1e-3, 'adamd_debias_term': True}, 50),
    (RAdam, {'lr': 1e-1, 'weight_decay': 1e-3, 'adamd_debias_term': True}, 100),
    (Ranger, {'lr': 5e-1, 'weight_decay': 1e-3, 'adamd_debias_term': True}, 100),
    (Ranger21, {'lr': 5e-1, 'weight_decay': 1e-3, 'adamd_debias_term': True, 'num_iterations': 200}, 200),
    (AdaPNM, {'lr': 3e-1, 'weight_decay': 1e-3, 'adamd_debias_term': True}, 50),
]

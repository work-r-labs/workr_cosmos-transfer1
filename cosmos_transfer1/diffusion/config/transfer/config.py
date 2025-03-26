# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any, List

import attrs

from cosmos_transfer1.diffusion.config.transfer.model import CtrlModelConfig
from cosmos_transfer1.diffusion.config.transfer.registry import register_configs
from cosmos_transfer1.diffusion.model.model_ctrl import VideoDiffusionModelWithCtrl
from cosmos_transfer1.utils import config
from cosmos_transfer1.utils.config_helper import import_all_modules_from_package
from cosmos_transfer1.utils.lazy_config import PLACEHOLDER
from cosmos_transfer1.utils.lazy_config import LazyCall as L
from cosmos_transfer1.utils.lazy_config import LazyDict


@attrs.define(slots=False)
class Config(config.Config):
    # default config groups that will be used unless overwritten
    # see config groups in registry.py
    defaults: List[Any] = attrs.field(
        factory=lambda: [
            "_self_",
            {"net": None},
            {"net_ctrl": None},
            {"hint_key": "control_input_edge"},
            {"conditioner": "ctrlnet_add_fps_image_size_padding_mask"},
            {"tokenizer": "vae1"},
            {"experiment": None},
        ]
    )
    model_obj: LazyDict = L(VideoDiffusionModelWithCtrl)(
        config=PLACEHOLDER,
    )


def make_config():
    c = Config(
        model=CtrlModelConfig(),
    )
    register_configs()

    import_all_modules_from_package("cosmos_transfer1.diffusion.config.inference")
    return c

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

# Cosmos Transfer1 Model Checkpoints
COSMOS_TRANSFER1_7B_CHECKPOINT = "nvidia/Cosmos-Transfer1-7B"
COSMOS_TRANSFER1_7B_SAMPLE_AV_CHECKPOINT = "nvidia/Cosmos-Transfer1-7B-Sample-AV"
COSMOS_TOKENIZER_CHECKPOINT = "nvidia/Cosmos-Tokenize1-CV8x8x8-720p"

# 3rd Party Model Checkpoints
SAM2_MODEL_CHECKPOINT = "facebook/sam2-hiera-large"
DEPTH_ANYTHING_MODEL_CHECKPOINT = "depth-anything/Depth-Anything-V2-Small-hf"
GROUNDING_DINO_MODEL_CHECKPOINT = "IDEA-Research/grounding-dino-tiny"
T5_MODEL_CHECKPOINT = "google-t5/t5-11b"

# Internal Checkpoint Paths, please append _PATH to the end of the variable
BASE_7B_CHECKPOINT_PATH = f"{COSMOS_TRANSFER1_7B_CHECKPOINT}/base_model.pt"
VIS2WORLD_CONTROLNET_7B_CHECKPOINT_PATH = f"{COSMOS_TRANSFER1_7B_CHECKPOINT}/vis_control.pt"
EDGE2WORLD_CONTROLNET_7B_CHECKPOINT_PATH = f"{COSMOS_TRANSFER1_7B_CHECKPOINT}/edge_control.pt"
SEG2WORLD_CONTROLNET_7B_CHECKPOINT_PATH = f"{COSMOS_TRANSFER1_7B_CHECKPOINT}/seg_control.pt"
DEPTH2WORLD_CONTROLNET_7B_CHECKPOINT_PATH = f"{COSMOS_TRANSFER1_7B_CHECKPOINT}/depth_control.pt"
UPSCALER_CONTROLNET_7B_CHECKPOINT_PATH = f"{COSMOS_TRANSFER1_7B_CHECKPOINT}/4kupscaler_control.pt"
GUARDRAIL_CHECKPOINT_PATH = f"{COSMOS_TRANSFER1_7B_CHECKPOINT}/guardrail"
BASE_7B_CHECKPOINT_AV_SAMPLE_PATH = f"{COSMOS_TRANSFER1_7B_SAMPLE_AV_CHECKPOINT}/base_model.pt"
HDMAP2WORLD_CONTROLNET_7B_CHECKPOINT_PATH = f"{COSMOS_TRANSFER1_7B_SAMPLE_AV_CHECKPOINT}/hdmap_control.pt"
LIDAR2WORLD_CONTROLNET_7B_CHECKPOINT_PATH = f"{COSMOS_TRANSFER1_7B_SAMPLE_AV_CHECKPOINT}/lidar_control.pt"

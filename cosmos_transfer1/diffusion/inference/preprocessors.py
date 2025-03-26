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

import json
import os

from cosmos_transfer1.auxiliary.depth_anything.model.depth_anything import DepthAnythingModel
from cosmos_transfer1.auxiliary.sam2.sam2_model import VideoSegmentationModel
from cosmos_transfer1.utils import log


class Preprocessors:
    def __init__(self):
        self.depth_model = None
        self.seg_model = None

    def __call__(self, input_video, input_prompt, control_inputs, output_folder):
        for hint_key in control_inputs:
            if hint_key in ["depth", "seg"]:
                self.gen_input_control(input_video, input_prompt, hint_key, control_inputs[hint_key], output_folder)

            # for all hints we need to create weight tensor if not present
            control_input = control_inputs[hint_key]

            # For each control input modality, compute a spatiotemporal weight tensor as long as
            # the user provides "control_weight_prompt". The object specified in the
            # control_weight_prompt will be treated as foreground and have control_weight for these locations.
            # Everything else will be treated as background and have control weight 0 at those locations.
            if control_input.get("control_weight_prompt", None) is not None:
                prompt = control_input["control_weight_prompt"]
                log.info(f"{hint_key}: generating control weight tensor with SAM using {prompt=}")
                out_tensor = os.path.join(output_folder, f"{hint_key}_control_weight.pt")
                out_video = os.path.join(output_folder, f"{hint_key}_control_weight.mp4")
                weight_scaler = (
                    control_input["control_weight"] if isinstance(control_input["control_weight"], float) else 1.0
                )
                self.segmentation(
                    in_video=input_video,
                    out_tensor=out_tensor,
                    out_video=out_video,
                    prompt=prompt,
                    weight_scaler=weight_scaler,
                    binarize_video=True,
                )
        return control_inputs

    def gen_input_control(self, in_video, in_prompt, hint_key, control_input, output_folder):
        # if input control isn't provided we need to run preprocessor to create input control tensor
        # for depth no special params, for SAM we need to run with prompt
        if control_input.get("input_control", None) is None:
            out_video = os.path.join(output_folder, f"{hint_key}_input_control.mp4")
            control_input["input_control"] = out_video
            if hint_key == "seg":
                prompt = control_input.get("input_control_prompt", in_prompt)
                prompt = " ".join(prompt.split()[:128])
                log.info(
                    f"no input_control provided for {hint_key}. generating input control video with SAM using {prompt=}"
                )
                self.segmentation(
                    in_video=in_video,
                    out_video=out_video,
                    prompt=prompt,
                )
            else:
                log.info(
                    f"no input_control provided for {hint_key}. generating input control video with DepthAnythingModel"
                )
                self.depth(
                    in_video=in_video,
                    out_video=out_video,
                )

    def depth(self, in_video, out_video):
        if self.depth_model is None:
            self.depth_model = DepthAnythingModel()

        self.depth_model(in_video, out_video)

    def segmentation(
        self,
        in_video,
        prompt,
        out_video=None,
        out_tensor=None,
        weight_scaler=None,
        binarize_video=False,
    ):
        if self.seg_model is None:
            self.seg_model = VideoSegmentationModel()
        self.seg_model(
            input_video=in_video,
            output_video=out_video,
            output_tensor=out_tensor,
            prompt=prompt,
            weight_scaler=weight_scaler,
            binarize_video=binarize_video,
        )


if __name__ == "__main__":
    control_inputs = dict(
        {
            "depth": {
                # "input_control": "depth_control_input.mp4",  # if empty we need to run depth
                # "control_weight" : "0.1", # if empty we need to run SAM
                "control_weight_prompt": "a boy",  # SAM weights prompt
            },
            "seg": {
                # "input_control": "seg_control_input.mp4",  # if empty we need to run SAM
                "input_control_prompt": "A boy",
                "control_weight_prompt": "A boy",  # if present we need to generate weight tensor
            },
        },
    )

    preprocessor = Preprocessors()
    input_video = "cosmos_transfer1/models/sam2/assets/input_video.mp4"

    preprocessor(input_video, control_inputs)
    print(json.dumps(control_inputs, indent=4))

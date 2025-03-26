# Sample-AV Transfer

## Install Cosmos-Transfer1

### Environment setup

Cosmos runs only on Linux systems. We have tested the installation with Ubuntu 24.04, 22.04, and 20.04.
Cosmos requires the Python version to be `3.10.x`. Please also make sure you have `conda` installed ([instructions](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)).

```bash
# Clone the repo
git clone git@github.com:nvidia-cosmos/cosmos-transfer1.git
cd cosmos-transfer1
git submodule update --init --recursive
# Create the cosmos-transfer1 conda environment.
conda env create --file cosmos-transfer1.yaml
# Activate the cosmos-transfer1 conda environment.
conda activate cosmos-transfer1
# Install the dependencies.
pip install -r requirements.txt
# Patch Transformer engine linking issues in conda environments.
ln -sf $CONDA_PREFIX/lib/python3.10/site-packages/nvidia/*/include/* $CONDA_PREFIX/include/
ln -sf $CONDA_PREFIX/lib/python3.10/site-packages/nvidia/*/include/* $CONDA_PREFIX/include/python3.10
# Install Transformer engine.
pip install transformer-engine[pytorch]==1.12.0
```

You can test the environment setup with
```bash
CUDA_HOME=$CONDA_PREFIX PYTHONPATH=$(pwd) python scripts/test_environment.py
```

### Download Checkpoints

1. Generate a [Hugging Face](https://huggingface.co/settings/tokens) access token. Set the access token to 'Read' permission (default is 'Fine-grained').

2. Log in to Hugging Face with the access token:

```bash
huggingface-cli login
```

3. Accept the [LlamaGuard-7b terms](https://huggingface.co/meta-llama/LlamaGuard-7b)

4. Download the Cosmos model weights from [Hugging Face](https://huggingface.co/collections/nvidia/cosmos-transfer1-67c9d328196453be6e568d3e):

```bash
CUDA_HOME=$CONDA_PREFIX PYTHONPATH=$(pwd) python scripts/download_checkpoints.py --output_dir checkpoints/
```

Note that this will require about 300GB of free storage. Not all these checkpoints will be used in every generation.

5. The downloaded files should be in the following structure:

```
checkpoints/
├── nvidia
│   ├── Cosmos-Transfer1-7B
│   │   ├── base_model.pt
│   │   ├── vis_control.pt
│   │   ├── edge_control.pt
│   │   ├── seg_control.pt
│   │   ├── depth_control.pt
│   │   ├── 4kupscaler_control.pt
│   │   ├── config.json
│   │   └── guardrail
│   │       ├── aegis/
│   │       ├── blocklist/
│   │       ├── face_blur_filter/
│   │       └── video_content_safety_filter/
│   │
│   ├── Cosmos-Transfer1-7B-Sample-AV/
│   │   ├── base_model.pt
│   │   ├── hdmap_control.pt
│   │   └── lidar_control.pt
│   │
│   └── Cosmos-Tokenize1-CV8x8x8-720p
│       ├── decoder.jit
│       ├── encoder.jit
│       ├── autoencoder.jit
│       └── mean_std.pt
│
├── depth-anything/...
├── facebook/...
├── google-t5/...
└── IDEA-Research/
```

## Run Example

For a general overview of how to use the model see [this guide](inference_cosmos_transfer1_7b.md).

This is an example of post-training Cosmos-Transfer1 using autonomous vehicle (AV) data. Here we provide two controlnets, `hdmap` and `lidar`, that allow transfering from those domains to the real world.

Ensure you are at the root of the repository before executing the following:

```bash
#!/bin/bash
export PROMPT="The video is captured from a camera mounted on a car. The camera is facing forward. The video showcases a scenic golden-hour drive through a suburban area, bathed in the warm, golden hues of the setting sun. The dashboard camera captures the play of light and shadow as the sun’s rays filter through the trees, casting elongated patterns onto the road. The streetlights remain off, as the golden glow of the late afternoon sun provides ample illumination. The two-lane road appears to shimmer under the soft light, while the concrete barrier on the left side of the road reflects subtle warm tones. The stone wall on the right, adorned with lush greenery, stands out vibrantly under the golden light, with the palm trees swaying gently in the evening breeze. Several parked vehicles, including white sedans and vans, are seen on the left side of the road, their surfaces reflecting the amber hues of the sunset. The trees, now highlighted in a golden halo, cast intricate shadows onto the pavement. Further ahead, houses with red-tiled roofs glow warmly in the fading light, standing out against the sky, which transitions from deep orange to soft pastel blue. As the vehicle continues, a white sedan is seen driving in the same lane, while a black sedan and a white van move further ahead. The road markings are crisp, and the entire setting radiates a peaceful, almost cinematic beauty. The golden light, combined with the quiet suburban landscape, creates an atmosphere of tranquility and warmth, making for a mesmerizing and soothing drive."
export CUDA_VISIBLE_DEVICES=0
export CHECKPOINT_DIR="${CHECKPOINT_DIR:=./checkpoints}"
CUDA_HOME=$CONDA_PREFIX PYTHONPATH=$(pwd) python cosmos_transfer1/diffusion/inference/transfer.py \
    --checkpoint_dir $CHECKPOINT_DIR \
    --video_save_name output_video \
    --video_save_folder outputs/sample_av_multi_control \
    --prompt "$PROMPT" \
    --sigma_max 80 \
    --offload_text_encoder_model --is_av_sample \
    --controlnet_specs assets/sample_av_multi_control_spec.json
```

This launches `transfer.py` and configures the controlnets for inference according to `assets/sample_av_multi_control_spec.json`:

```json
{
    "hdmap": {
        "control_weight": 0.3,
        "input_control": "assets/sample_av_multi_control_input_hdmap.mp4"
    },
    "lidar": {
        "control_weight": 0.7,
        "input_control": "assets/sample_av_multi_control_input_lidar.mp4"
    }
}
```

Note that unlike other examples, here we chose to provide the input prompt and some other parameters through the command line arguments, as opposed to through the spec file. This flexibility allows abstracting out the fixed parameters in the spec file and vary the dynamic parameters through the command line.

### Additional Toolkits
We provide the `cosmos-av-sample-toolkits` at https://github.com/nv-tlabs/cosmos-av-sample-toolkits.

This toolkit includes:

- 10 additional raw data samples (e.g., HDMap and LiDAR), along with scripts to preprocess and render them into model-compatible inputs.
- Rendering scripts for converting other datasets, such as the Waymo Open Dataset, into inputs compatible with Cosmos-Transfer1.

### The input and output videos

HDMap input control:

<video src="https://github.com/user-attachments/assets/f105c843-811a-4b6b-99f6-9136a8e1b601">
  Your browser does not support the video tag.
</video>


LiDAR input control:

<video src="https://github.com/user-attachments/assets/a1beed14-9ade-4e47-a94e-1f9ca41b59a7">
  Your browser does not support the video tag.
</video>


Output video using HDMap and LiDAR:

<video src="https://github.com/user-attachments/assets/82ce1d89-63c7-402d-aae4-a7f1c6358cae">
  Your browser does not support the video tag.
</video>

Feel free to experiment with more specs. For example, the command below only uses HDMap:

```bash
export PROMPT="The video is captured from a camera mounted on a car. The camera is facing forward. The video showcases a scenic golden-hour drive through a suburban area, bathed in the warm, golden hues of the setting sun. The dashboard camera captures the play of light and shadow as the sun’s rays filter through the trees, casting elongated patterns onto the road. The streetlights remain off, as the golden glow of the late afternoon sun provides ample illumination. The two-lane road appears to shimmer under the soft light, while the concrete barrier on the left side of the road reflects subtle warm tones. The stone wall on the right, adorned with lush greenery, stands out vibrantly under the golden light, with the palm trees swaying gently in the evening breeze. Several parked vehicles, including white sedans and vans, are seen on the left side of the road, their surfaces reflecting the amber hues of the sunset. The trees, now highlighted in a golden halo, cast intricate shadows onto the pavement. Further ahead, houses with red-tiled roofs glow warmly in the fading light, standing out against the sky, which transitions from deep orange to soft pastel blue. As the vehicle continues, a white sedan is seen driving in the same lane, while a black sedan and a white van move further ahead. The road markings are crisp, and the entire setting radiates a peaceful, almost cinematic beauty. The golden light, combined with the quiet suburban landscape, creates an atmosphere of tranquility and warmth, making for a mesmerizing and soothing drive."
export CUDA_VISIBLE_DEVICES=0
export CHECKPOINT_DIR="${CHECKPOINT_DIR:=./checkpoints}"
CUDA_HOME=$CONDA_PREFIX PYTHONPATH=$(pwd) python cosmos_transfer1/diffusion/inference/transfer.py \
    --checkpoint_dir $CHECKPOINT_DIR \
    --video_save_name output_video \
    --video_save_folder outputs/sample_av_hdmap_spec \
    --prompt "$PROMPT" \
    --offload_text_encoder_model --is_av_sample \
    --controlnet_specs assets/sample_av_hdmap_spec.json
```

[comment]: <> (This README.md was generated by tools/collect_metrics.py.)
[comment]: <> (Please modify docs/README.md.in and/or collect_metrics.py to make permanent changes.)

# PyTorch 2.0 TTNN Compiler
This project allows to run PyTorch code on [Tenstorrent](https://tenstorrent.com/) hardware.

## Supported Models

The table below summarizes the results of running various ML models through our TTNN compiler. For each model, we track whether the run was successful, the number of operations before and after conversion, the number of `to_device` and `from_device` operations, performance metrics, and accuracy.

| Model                               | Run Success   | Torch Ops Before (Unique Ops)   | Torch Ops Remain (Unique Ops)   |   To/From Device Ops |   Original Run Time (ms) | Compiled Run Time (ms)   | Accuracy (%)   |
|:------------------------------------|:--------------|:--------------------------------|:--------------------------------|---------------------:|-------------------------:|:-------------------------|:---------------|
| [Mnist (Eval)](tests/models/mnist)  | ✅            | 14 (8)                          | 5 (4)                           |                   16 |                    35.53 | 556.63                   | 99.72          |
| [Mnist (Train)](tests/models/mnist) | ✅            | 14 (8)                          | 7 (5)                           |                   14 |                   114.16 | 3076.17                  | 76.59          |
| [ResNet18](tests/models/resnet)     | ✅            | 70 (9)                          | 42 (4)                          |                   44 |                  2023.95 | 10673.42                 | 99.99          |
| [Bloom](tests/models/bloom)         | ✅            | 1407 (29)                       | 626 (11)                        |                 1378 |                 28504    | 68025.6                  | 45.77          |
| [YOLOS](tests/models/yolos)         | ✅            | 964 (28)                        | 320 (11)                        |                  825 |                  1340.21 | 46101.1                  | 71.71          |
| [Llama](tests/models/llama)         | ✅            | 3 (2)                           | 2 (2)                           |                    2 |                164063    | 166348.21                | 100.0          |
| [BERT](tests/models/bert)           | ✅            | 1393 (21)                       | 491 (5)                         |                 1465 |                 63591.6  | 55096.44                 | 98.64          |
| [Falcon](tests/models/falcon)       | ✘             | 3 (3)                           | 2 (2)                           |                    5 |                 46268.6  | N/A                      | N/A            |
| [GPT-2](tests/models/gpt2)          | ✘             | 748 (31)                        | 307 (12)                        |                  644 |                  1793.52 | N/A                      | N/A            |

### Explanation of Metrics

**Model**: Name of the model.  
**Run Success**: Indicates whether the model runs successfully after conversion.  
**Torch Ops Before (Unique Ops)**: The total number of operations used by the model in the original Torch implementation. The number in parenthesis represents the total unique ops.  
**Torch Ops Remain (Unique Ops)**: The total number of operations used after conversion to TTNN. The number in parenthesis represents the total unique ops.  
**To/From Device Ops**: The number of `to/from_device` operations (data transfer to/from the device).  
**Original Run Time (ms)**: Execution time (in seconds) of the model before conversion.  
**Compiled Run Time (ms)**: Execution time (in seconds) of the model after conversion.  
**Accuracy (%)**: Model accuracy on a predefined test dataset after conversion.  
***
**NOTE:** The total number of ops currently reflect only the first graph of a model. This will be fixed in a future update to include all graphs.  

***

### Op conversion status per model

#### Mnist (Eval)
| aten ops                             | status   |   count |
|:-------------------------------------|:---------|--------:|
| aten._log_softmax.default            | ✘        |       1 |
| aten.addmm.default                   | ✅       |       2 |
| aten.clone.default                   | ✅       |       2 |
| aten.convolution.default             | ✘        |       2 |
| aten.max_pool2d_with_indices.default | ✘        |       1 |
| aten.relu.default                    | ✅       |       3 |
| aten.t.default                       | ✅       |       2 |
| aten.view.default                    | ✅       |       1 |
#### Mnist (Train)
| aten ops                             | status   |   count |
|:-------------------------------------|:---------|--------:|
| aten._log_softmax.default            | ✘        |       1 |
| aten.addmm.default                   | ✅       |       2 |
| aten.convolution.default             | ✘        |       2 |
| aten.max_pool2d_with_indices.default | ✘        |       1 |
| aten.native_dropout.default          | ✘        |       2 |
| aten.relu.default                    | ✅       |       3 |
| aten.t.default                       | ✅       |       2 |
| aten.view.default                    | ✅       |       1 |
#### ResNet18
| aten ops                                          | status   |   count |
|:--------------------------------------------------|:---------|--------:|
| aten._native_batch_norm_legit_no_training.default | ✘        |      20 |
| aten.add.Tensor                                   | ✅       |       8 |
| aten.addmm.default                                | ✅       |       1 |
| aten.convolution.default                          | ✘        |      20 |
| aten.max_pool2d_with_indices.default              | ✘        |       1 |
| aten.mean.dim                                     | ✅       |       1 |
| aten.relu.default                                 | ✅       |      17 |
| aten.t.default                                    | ✅       |       1 |
| aten.view.default                                 | ✅       |       1 |
#### Bloom
| aten ops                       | status   |   count |
|:-------------------------------|:---------|--------:|
| aten._softmax.default          | ✅       |      24 |
| aten._to_copy.default          | ✘        |      54 |
| aten._unsafe_view.default      | ✘        |      24 |
| aten.add.Tensor                | ✅       |      96 |
| aten.addmm.default             | ✅       |      96 |
| aten.arange.start              | ✘        |       1 |
| aten.baddbmm.default           | ✅       |      24 |
| aten.bmm.default               | ✅       |      24 |
| aten.clone.default             | ✅       |      96 |
| aten.cumsum.default            | ✘        |       1 |
| aten.embedding.default         | ✅       |       1 |
| aten.expand.default            | ✅       |       2 |
| aten.full.default              | ✅       |       1 |
| aten.lift_fresh_copy.default   | ✘        |       1 |
| aten.masked_fill.Scalar        | ✘        |      26 |
| aten.mm.default                | ✅       |       1 |
| aten.mul.Tensor                | ✅       |     146 |
| aten.native_layer_norm.default | ✅       |      50 |
| aten.permute.default           | ✅       |      48 |
| aten.pow.Tensor_Tensor         | ✘        |       1 |
| aten.rsub.Scalar               | ✅       |       1 |
| aten.select.int                | ✘        |      72 |
| aten.slice.Tensor              | ✘        |      78 |
| aten.sub.Tensor                | ✅       |       1 |
| aten.t.default                 | ✅       |      97 |
| aten.tanh.default              | ✅       |      24 |
| aten.transpose.int             | ✅       |      48 |
| aten.unsqueeze.default         | ✘        |       6 |
| aten.view.default              | ✅       |     363 |
#### YOLOS
| aten ops                       | status   |   count |
|:-------------------------------|:---------|--------:|
| aten._softmax.default          | ✅       |      12 |
| aten._to_copy.default          | ✘        |       2 |
| aten._unsafe_index.Tensor      | ✘        |      16 |
| aten.add.Tensor                | ✅       |      71 |
| aten.addmm.default             | ✅       |      78 |
| aten.arange.default            | ✘        |       4 |
| aten.bmm.default               | ✅       |      24 |
| aten.cat.default               | ✘        |       2 |
| aten.clamp.default             | ✅       |      32 |
| aten.clone.default             | ✅       |      50 |
| aten.convolution.default       | ✘        |       1 |
| aten.div.Tensor                | ✘        |      12 |
| aten.expand.default            | ✅       |      50 |
| aten.floor.default             | ✘        |       2 |
| aten.gelu.default              | ✅       |      12 |
| aten.mul.Tensor                | ✅       |      82 |
| aten.native_layer_norm.default | ✅       |      25 |
| aten.permute.default           | ✅       |      48 |
| aten.relu.default              | ✅       |       4 |
| aten.rsub.Scalar               | ✘        |      10 |
| aten.select.int                | ✘        |       1 |
| aten.sigmoid.default           | ✅       |       1 |
| aten.slice.Tensor              | ✘        |      12 |
| aten.sub.Tensor                | ✅       |      36 |
| aten.t.default                 | ✅       |      78 |
| aten.transpose.int             | ✅       |      15 |
| aten.unsqueeze.default         | ✅       |       1 |
| aten.view.default              | ✅       |     283 |
#### Llama
| aten ops               | status   |   count |
|:-----------------------|:---------|--------:|
| aten.slice.Tensor      | ✘        |       1 |
| aten.unsqueeze.default | ✘        |       2 |
#### BERT
| aten ops                       | status   |   count |
|:-------------------------------|:---------|--------:|
| aten._softmax.default          | ✅       |      24 |
| aten._to_copy.default          | ✘        |       1 |
| aten.add.Tensor                | ✅       |      74 |
| aten.addmm.default             | ✅       |     145 |
| aten.bmm.default               | ✅       |      48 |
| aten.clone.default             | ✅       |      99 |
| aten.div.Tensor                | ✅       |      24 |
| aten.embedding.default         | ✅       |       3 |
| aten.expand.default            | ✅       |      96 |
| aten.gelu.default              | ✅       |      24 |
| aten.mul.Tensor                | ✅       |       1 |
| aten.native_layer_norm.default | ✅       |      49 |
| aten.permute.default           | ✅       |      96 |
| aten.rsub.Scalar               | ✅       |       1 |
| aten.slice.Tensor              | ✘        |       4 |
| aten.split.Tensor              | ✘        |       1 |
| aten.squeeze.dim               | ✘        |       2 |
| aten.t.default                 | ✅       |     145 |
| aten.transpose.int             | ✅       |      24 |
| aten.unsqueeze.default         | ✅       |       2 |
| aten.view.default              | ✅       |     530 |
#### Falcon
| aten ops               | status   |   count |
|:-----------------------|:---------|--------:|
| aten.arange.start      | ✘        |       1 |
| aten.embedding.default | ✅       |       1 |
| aten.unsqueeze.default | ✅       |       1 |
#### GPT-2
| aten ops                       | status   |   count |
|:-------------------------------|:---------|--------:|
| aten._softmax.default          | ✅       |      12 |
| aten._to_copy.default          | ✘        |       2 |
| aten.add.Tensor                | ✅       |      61 |
| aten.addmm.default             | ✅       |      48 |
| aten.arange.default            | ✘        |       1 |
| aten.arange.start              | ✘        |       1 |
| aten.argmax.default            | ✘        |       1 |
| aten.bmm.default               | ✅       |      24 |
| aten.clone.default             | ✅       |      49 |
| aten.div.Tensor                | ✅       |      12 |
| aten.embedding.default         | ✅       |       2 |
| aten.eq.Scalar                 | ✅       |       1 |
| aten.expand.default            | ✅       |      48 |
| aten.full.default              | ✘        |      24 |
| aten.index.Tensor              | ✘        |       1 |
| aten.mm.default                | ✅       |       1 |
| aten.mul.Tensor                | ✅       |      49 |
| aten.native_layer_norm.default | ✅       |      25 |
| aten.permute.default           | ✅       |      48 |
| aten.pow.Tensor_Scalar         | ✅       |      12 |
| aten.remainder.Scalar          | ✘        |       1 |
| aten.rsub.Scalar               | ✅       |       1 |
| aten.slice.Tensor              | ✘        |      50 |
| aten.split.Tensor              | ✘        |      12 |
| aten.sub.Tensor                | ✘        |       1 |
| aten.t.default                 | ✅       |       1 |
| aten.tanh.default              | ✅       |      12 |
| aten.transpose.int             | ✅       |      12 |
| aten.unsqueeze.default         | ✅       |       3 |
| aten.view.default              | ✅       |     221 |
| aten.where.self                | ✘        |      12 |


## Quickstart

The `torch_ttnn` module has a `backend` function, which can be used with the `torch.compile()`.

```python
import torch
import torch_ttnn

# A torch Module
class FooModule(torch.nn.Module):
    ...
# Create a module
module = FooModule()

# Compile the module, with ttnn backend
device = ttnn.open_device(device_id=0)
option = torch_ttnn.TorchTtnnOption(device=self.device)
ttnn_module = torch.compile(module, backend=torch_ttnn.backend, options=option)

# Running inference / training
ttnn_module(input_data)
```

## Tracer
The tracer dump the information of fx graph such as node's op_name and shape.

For example, you can run this script to parse the information
```
PYTHONPATH=$(pwd) python3 tools/stat_models.py --trace_orig --backward --profile
ls stat/raw
```

By default, the raw result will be stored at `stat/raw`, and you can run this script to generate the report
```
python3 tools/generate_report.py
ls stat/
```
Now the `stat/` folder have these report
 - `fw_node_count.csv`
 - `bw_node_count.csv`
 - `fw_total_input_size_dist/`
 - `bw_total_input_size_dist/`
 - `fw_total_output_size_dist/`
 - `bw_total_output_size_dist/`
 - `profile/`

The `node_count.csv` show the node with `op_type` appear in the fx graph. This report can help analyze the frequency of op type appear in the graph.

The `*_total_*_size_dist/` statistics the `op_type`'s input/output_size distribution from all fx graph recored in `stat/raw`. This report can help analyze the memory footprint durning the calculation of `op_type`.

 - Notice: the default `input_shapes` in `tools/stat_torchvision.py` is `[1,3,224,224]`, which has dependency with `*_total_*_size_dist/` report.

 - Notice: the [aten ir interface is in there](https://pytorch.org/docs/stable/torch.compiler_ir.html)

[The `profile/` is the tools provided by pytorch](https://pytorch.org/tutorials/recipes/recipes/profiler_recipe.html), you can open it by the url: chrome://tracing


# For developers

## Install torch-ttnn with editable mode

During development, you may want to use the torch-ttnn package for testing.
In order to do that, you can install the torch-ttnn package in "editable"
mode with

```shell
pip install -e .
```

Now, you can utilize `torch_ttnn` in your Python code. Any modifications you make to the `torch_ttnn` package will take effect immediately, eliminating the need for constant reinstallation via pip.

## Build wheel file

For developers want to deploy the wheel, you can build the wheel file with

```shell
python -m build
```

Then you can upload the `.whl` file to the PyPI (Python Package Index).

## Run transformer models
To run transformer model with ttnn backend, run:
```
PYTHONPATH="$TT_METAL_HOME:$(pwd)" python3 tools/run_transformers.py --model "phiyodr/bert-large-finetuned-squad2" --backend torch_ttnn
```

You can also substitute the backend with `torch_stat` to run a reference comparison.

# Add a model test
If you want to record run time metrics for a model or test, include a Pytest fixture named `record_property` as a parameter and set the "model_name" key.  
If you also want to compile the model with torch_ttnn backend, set the "torch_ttnn" key to a tuple in this order `(model, test_inputs, outputs)`. "model_name" still needs to be set. See the example code snippet below. Currently, only `torch.nn.Module` models with a `forward` function are supported.
```
def Model(torch.nn.Module):
    def forward(self, x):
        # ...
        return outputs

# Add "record_property" parameter
def test_model_name(record_property):
    # Should be set as early as possible
    record_property("model_name", "Model Name")

    model = Model()
    # ...
    outputs = model(test_input)
    # outputs = model(**test_inputs) # dictionary inputs are also supported
    # ...

    # Can be set once all three objects for the tuple are defined
    record_property("torch_ttnn", (model, test_input(s), outputs))
```


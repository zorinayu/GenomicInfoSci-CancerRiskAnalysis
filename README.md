---
license: odc-by
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
dataset_info:
  features:
  - name: image
    dtype: image
  - name: identifier
    dtype: string
  - name: label
    dtype: string
  - name: sex
    dtype: string
  - name: age
    dtype: int64
  - name: sfreq
    dtype: float64
  splits:
  - name: train
    num_bytes: 1732399128.184
    num_examples: 11928
  download_size: 1879284196
  dataset_size: 1732399128.184
---

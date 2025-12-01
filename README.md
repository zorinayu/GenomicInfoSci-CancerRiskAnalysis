# GenomicInfoSci-CancerRiskAnalysis

Comparative Modeling of Somatic Mutation Accumulation for Age-Dependent Cancer Risk

## 测试入口

运行所有测试：
```bash
python -m pytest tests/
```

运行特定测试：
```bash
python -m pytest tests/test_models.py
python -m pytest tests/test_utils.py
```

## 运行项目

```bash
# 安装依赖
pip install -r requirements.txt

# 运行notebook
jupyter notebook notebooks/visualization_examples.ipynb
```

## 引用 (References)

### Model B: Replicative-Risk Baseline (LSCD-based Model)

- **Tomasetti, C., & Vogelstein, B. (2015)**. Variation in cancer risk among tissues can be explained by the number of stem cell divisions. *Science*, 347(6217), 78-81.
  - DOI: https://doi.org/10.1126/science.1260825
  - URL: https://www.science.org/doi/10.1126/science.1260825

### Model C: Deterministic Hazard Model / Cox Regression

- **Cox, D. R. (1972)**. Regression Models and Life-Tables. *Journal of the Royal Statistical Society, Series B*, 34(2), 187-220.
  - DOI: https://doi.org/10.1111/j.2517-6161.1972.tb00899.x

- **lifelines Library**: Davidson-Pilon, C. (2019). lifelines: survival analysis in Python. *Journal of Open Source Software*, 4(40), 1317.
  - GitHub: https://github.com/CamDavidsonPilon/lifelines
  - Documentation: https://lifelines.readthedocs.io/

更多引用信息请参见 `ref/REFERENCES.md`

# [Method-Evolution-Tracker](https://github.com/tian-2024/Method-Evolution-Tracker)

A tool to track and analyze the evolution of research methods based on paper comparisons.

This project is already deployed on **Github Actions**, every time the `input.md` is updated, the `output.md` will be updated automatically.

## Overview

To run the method evolution tracker, execute the following command:

```bash
python run_tracker.py --transitive
```

### Input Format

The input is a markdown file `input.md` with the following format:
```
method1>baseline1,baseline2,...
method2>baseline1,baseline2,...
```
For example:
```
LEDITS++>SDEdit,Imagic,DDIM Inversion,Pix2Pix-Zero,DiffEdit,DDPM Inversion
DDPM Inversion>PnP,EDICT,null-text inversion,CycleDiffusion
```

which means:

- In paper **LEDITS++**, it outperforms methods **SDEdit**, **Imagic**, **DDIM Inversion**, **Pix2Pix-Zero**, **DiffEdit**, **DDPM Inversion**.
- In paper **DDPM Inversion**, it outperforms methods **PnP**, **EDICT**, **null-text inversion**, **CycleDiffusion**.

### Output Format

The output is a markdown file `output.md` with the following format:

| Method  | Better Methods          |
| ------- | ----------------------- |
| method1 | baseline1,baseline2,... |


For example:

| Method         | Better Methods                           |
| -------------- | ---------------------------------------- |
| CycleDiffusion | DDPM Inversion, LEDITS++                 |
| DDIB           | CycleDiffusion, DDPM Inversion, LEDITS++ |


which means:
- after method **CycleDiffusion** is proposed, subsequent methods like **DDPM Inversion**, **LEDITS++** are considered superior. 
- The tool helps track the progression of method **CycleDiffusion** over time.


## Environment

- **Python**: 3.10

## Parameters

- `--verbose`: Enable detailed process information during execution. This can help debug or understand the underlying analysis steps.
  
  Example:
  ```bash
  python run_tracker.py --verbose
  ```

- `--transitive`: Whether to compute transitive closure. For example, if **xx** is better than **yy**, and **yy** is better than **zz**, this flag will consider **xx** as better than **zz** as well. By default, this is set to `False`, which means only the direct comparisons stated in the papers are considered.
  
  Example:
  ```bash
  python run_tracker.py --transitive
  ```


## Contributing

Feel free to fork this repository, contribute bug fixes, or propose new features via pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
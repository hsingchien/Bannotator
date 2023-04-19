### Install guide

1. Install Git
2. In git bash, run

```bash
git clone https://github.com/hsingchien/Bannotator.git
```

3. In anaconda prompt, go to annotator directory, run

```bash
conda env create -f environment.yml
```

4. Then activate the environment

```bash
conda activate bannotator
```

5. Under this environment, go to the bannotator directory, run

```bash
python setup.py develop
```

6. To open the app, under this environment, run

```bash
annotate-behavior
```

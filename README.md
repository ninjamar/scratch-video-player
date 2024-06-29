# Scratch Video Player

These are some scripts I used to generate the data from my [scratch video player](https://scratch.mit.edu/projects/602626065/)


# Usage
Get a gif
```bash
bash conv.sh input.gif inputDimensions generated.gif outputDimensions
python3 make.py generated.gif WIDTHxHEIGHT output.txt

```
### Example

```bash
bash conv.sh rickroll.gif 1280x720 small.gif 96x54
python3 make.py small.gif 96x54 rickroll.txt

```

Upload the generated txt file to the list `data` in the [scratch video player](https://scratch.mit.edu/projects/602626065/). Apparently scratch stores lists twice in the project.json, so the generated text file has to be less than 2.5 mb.
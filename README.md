Chingolo Bot
============

Silly shitpost.

## Installing

We use python3 so install it bro.

```bash
mkvirtualenv --python=<path-to-python3-bin> chigolo_bot
pip3 install -r requirements.txt
```

Then use `workon chingolo_bot` and `deactivate`
to enter and exit the virtualenv.

## Running

From the virtualenv:

```bash
python run.py
```

## Testing

Inside the virtualenv run `python` and just
import `commands`. For example:

```python
import commands

commands.sadness()
> ('photo',
   {'caption': 'The Aesthetic of Jazz Cup  Jazz Cup photo to painting filter by Dreamscope.',
    'photo': 'https://65.media.tumblr.com/fe24f47ae83b344e548e4b53dd9f7c10/tumblr_o06anyADVs1uf27e8o1_1280.jpg'})
```

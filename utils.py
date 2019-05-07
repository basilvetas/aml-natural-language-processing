#!/usr/bin/python

""" defines utility functions for use in jupyter notebook """
import glob
from os import remove
from os.path import dirname, realpath, join
from timeit import default_timer as timer
from tqdm import tqdm
import pandas as pd

cache_path = join(dirname(realpath(__file__)), '../cache/')
tqdm.pandas()

def save_to_cache(path, name, df, **kwargs):
  """ saves df to cache at path under given name """
  start = timer()
  tqdm.write(f'Caching {name} data...')

  if path.endswith('.pkl'):
    df.to_pickle(path, **kwargs)
  elif path.endswith('.hdf'):
    with pd.HDFStore(path, mode='w') as store:
      store.append(name, df, **kwargs)
  else:
    raise ValueError(f'Invalid file extension for path {path}')

  tqdm.write(f'Took {timer() - start:.2f} seconds to cache {name}')
  return


def load_from_cache(path, name, **kwargs):
  """ loads df from cache at path based on given name """
  start = timer()
  tqdm.write(f'Loading {name} data from cache...')
  if path.endswith('.pkl'):
    df = pd.read_pickle(path, **kwargs)
  elif path.endswith('.hdf'):
    df = pd.read_hdf(path, name, **kwargs)
  else:
    raise ValueError(f'Invalid file extension for path {path}')

  tqdm.write(f'Took {timer() - start:.2f} seconds to load {name} data')
  return df


def clear_cache(extensions):
  """ clears cached files of specified extension types """
  tqdm.write('Clearing cache...')
  cached_files = []
  if not extensions:
    extensions = ['hdf', 'pkl', 'tmp']

  for ext in extensions:
    cached_files.extend(glob.glob(join(cache_path, f'*.{ext}*'), recursive=True))

  for file in cached_files:
    remove(file)
  return
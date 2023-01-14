import toir
import click
from pathlib import Path

@click.command()
@click.argument('source', type=click.Path(exists=True, file_okay=False))
@click.argument('destination', type=click.Path(file_okay=False))
def extract(source, destination):
    source = Path(source)
    destination = Path(destination);

    l7cdir = source / 'toidata_release'
    if not l7cdir.exists() or not l7cdir.is_dir():
        print(f'path {l7cdir} does not exist or is not a directory')
        exit(-1)

    ebootpath = source / 'eboot.bin'
    if not ebootpath.exists():
        print(f'path {ebootpath} does not exist')

    destination.mkdir(parents=True, exist_ok=True)

    #toir.extract_eboot(ebootpath, destination)
    #toir.extract_dat(l7cdir, destination)
    #toir.extract_map_data(l7cdir, destination)
    #toir.extract_script(l7cdir, destination)
    #toir.extract_skits(l7cdir, destination)
    toir.extract_textures(l7cdir, destination)

if __name__ == '__main__':
    extract()
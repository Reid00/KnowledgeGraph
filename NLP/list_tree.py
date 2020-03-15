from pathlib import Path
import sys

def lst_tree(p,n):
    if p.is_file():
        print('|' + '\t|'*n + '-'*4 + p.name)
    elif p.is_dir():
        print('|' + '\t|'*n + '-'*4 + str(p.relative_to(p.parent)) + '\\')
        for pt in p.iterdir():
            lst_tree(pt,n+1)

if __name__ == "__main__":
    if len(sys.argv) != 1 and Path(sys.argv[1]).exists():
        lst_tree(Path(sys.argv[1]),0)
    else:
        lst_tree(Path('.'),0)
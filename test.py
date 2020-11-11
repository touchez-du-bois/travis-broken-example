import argparse
import re
import os
import shutil
import sys
from datetime import datetime
from tqdm import tqdm

def handle_commandline():
    parser = argparse.ArgumentParser()
    parser.add_argument('index',
        choices=HtmlCheck(),
        help="<index.html output>")
    args = parser.parse_args()
    return args.index

def process(untrans_html):
  path = os.getcwd()
  untrans = os.path.join(path,untrans_html)
  if os.path.isfile(untrans):
    return (untrans)
  else:
    raise ValueError('Error : 指定されたHTMLファイルが見つかりませんでした。HTMLファイルを指定してください。')

def backup(untrans):
    """Summary line.

    """
    dirname = os.path.dirname(untrans)
    basename = os.path.basename(untrans)
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    copyname = now + '_' + basename
    copy = shutil.copyfile(untrans,os.path.join(dirname,now + '_' + basename))
    if os.path.isfile(copy):
      return copy
    else:
      raise ValueError('Error : バックアップに失敗しました。処理を終了します。')

def convert(untrans):
    """Summary line.

    """
    langs = ['ja','zh','en']
    langsearch = ['','','']
    for i,lang in enumerate(tqdm(langs)):
      langsearch[i] = r'<div class="portal-content theme1" dir="ltr"><header class="portal-header" data-portal-language="'+ lang +'">.*?</footer></div>'
      data = open(trans, 'r', encoding='UTF-8',  newline='')
      transtext = data.read()
      if re.search(langsearch[i], str(transtext)):
          if langs[i] == 'ja':
              dropdown = r'<ul class="dropdown-menu">.*?</ul>'
              contents = re.search(dropdown, str(transtext))
          else:
              contents = re.search(langsearch[i], str(transtext))
          transcontent = contents.group()
          with open(untrans, encoding='UTF-8', newline='', mode='r') as f:
              untranstext = f.read()
              if re.search(langsearch[i], str(untranstext)):
                  if langs[i] == 'ja':
                      dropdown = r'<ul class="dropdown-menu">.*?</ul>'
                      contents = re.search(dropdown, str(untranstext))
                  else:
                      contents = re.search(langsearch[i], str(untranstext))
                  untranscontent = contents.group()
                  converted = untranstext.replace(untranscontent, transcontent)
              else:
                  if re.search(langsearch[i-1],str(untranstext)):
                      replaceslice = langsearch[i-1].replace('.*?</footer></div>','')
                      converted = untranstext.replace(replaceslice, transcontent + replaceslice)

      with open(untrans, encoding='UTF-8', newline='', mode='w') as f:
        try:
          f.write(converted)
          file = 'index.html'
        except NameError as e:
            print(e)
            raise ValueError('Error：index.htmlの置き換えに失敗しました。')
            sys.exit()

class HtmlCheck:

    def __contains__(self, val):
        if os.path.isfile(val) and val.endswith('.html'):
            return True
        elif os.path.isdir(val) and glob.glob(val + '/*.html'):
            return True


    def __iter__(self):
        return iter(('html',))


def main():
    untrans_html = handle_commandline()
    untrans = process(untrans_html)
    backup(untrans)
    print('Successfully copied contents')

if __name__ == "__main__":
    main()

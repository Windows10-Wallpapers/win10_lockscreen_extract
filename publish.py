import os
from PIL import Image
import git
from git import Repo
import func


def main():
    func.check_os()
    git_path = os.path.expanduser('~/Pictures/win10_lockscreen/')
    src_path = git_path + 'images/'
    if not os.path.isdir(src_path):
        print('Repository does not exist. Exit.')
        exit()
    original_files = [f for f in os.listdir(src_path) if f.endswith('.jpg')]

    thumb_path = git_path + 'thumbnails/'
    if not os.path.isdir(thumb_path):
        print('Thumbnail folder does not exist. Create new one.')
        os.mkdir(thumb_path)
    thumb_files = [f for f in os.listdir(thumb_path) if f.endswith('.jpg')]

    for fname in original_files:
        if fname in thumb_files:
            continue
        im = Image.open(src_path + fname)
        (x, y) = im.size
        h = 270
        w = x * h / y
        im.thumbnail((w, h), Image.ANTIALIAS)
        im.save(thumb_path + fname, 'JPEG')
        thumb_files += [fname]

    html_file = open(git_path + 'index.html', 'w')
    html_file.write('''<head>
<title>Windows 10 Lockscreens</title>
<script src="js/jquery-3.1.0.min.js"></script>
<script src="js/jquery.lazyload.js"></script>
<style>
a {
    text-decoration: none;
}
</style>
</head>
<div style="text-align:center;">
<h1>Windows 10 Lockscreens</h1>
<ul style="list-style-type: none;">
''')
    cnt = 1
    for fname in thumb_files:
        if cnt % 2:
            html_file.write('''    <li>
''')

        if 'land' in fname:
            w = 480
        if 'port' in fname:
            w = 151
        html_file.write('''        <a href=images/%s>
            <img class=lazy data-original=thumbnails/%s width=%s height=270>
        </a>
''' % (fname, fname, w))

        cnt += 1
        if cnt % 2:
            html_file.write('''</li>
<li>
''')
    html_file.write('''</ul>
</div>
<script>
$(function() {
    $('img.lazy').lazyload();
});
</script>
''')
    html_file.close()

    repo = Repo(git_path)
    repo.git.add('.')
    try:
        repo.git.commit('-m updated')
    except git.exc.GitCommandError:
        print('Nothing to commit. Exit.')
        exit()
    else:
        origin = repo.remote('origin')
        origin.push()

if __name__ == "__main__":
    main()
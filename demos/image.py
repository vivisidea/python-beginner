from PIL import Image
import os
import sys
 
# the color from black to white
CHARS = ('M', 'N', 'H', 'Q',
         '$', 'O', 'C', '?',
         '7', '&gt;', '!', ':',
         '-', ';', '.', ' ')
CHARS_COUNT = 16
# every 4 x 6 pixel matrix will be converted into a character
CHAR_WIDTH  = 2
CHAR_HEIGHT = 3
# the rate of char anime
RATE = 5
FONT_SIZE = 9
# output html and mp3 name
OUT_HTML_NAME = 'out.html'
OUT_MP3_NAME = 'out.mp3'
# output dir and temp dir
OUT_DIR = 'out'
TMP_DIR = 'tmp'
 
 
class CharacterBMP:
    '''
    Character bit map, load an image from path and convert it into html
    '''
    def __init__(self, path):
        '''
        path : path of image
        '''
        # load image and convert into grey scale image
        img = Image.open(path).convert('L')
 
        self.width = img.size[0]
        self.height = img.size[1]
        # get the data of pixels
        self.data = list(img.getdata())
        # print "width=%s, height=%s" % (self.width, self.height)
 
    def toHTML(self):
        '''
        convert to html
        '''
        str = ''
        for y in xrange(0, self.height, CHAR_HEIGHT):
            for x in xrange(0, self.width, CHAR_WIDTH):
                average = self._average(x, y)
                # map the grey scale value into chars
                charIndex = average / (256 / CHARS_COUNT)
                # print charIndex
                str = str + CHARS[charIndex]
            str = str + '<br/>'
 
        return str
 
    def _average(self, x, y):
        '''
        calculate the average grey scale of certain matrix
        and the size of matrix is CHAR_WIDTH x CHAR_HEIGHT
 
        x, y : start location of matrix
        '''
        sum = 0
        for j in xrange(CHAR_HEIGHT):
            for i in xrange(CHAR_WIDTH):
                sum = sum + self._getValue(x + i, y + j)
        return sum / (CHAR_HEIGHT * CHAR_WIDTH)
 
    def _getValue(self, x, y):
        '''
        get the grey scale value of certain point
        x, y : the location of point
        '''
        if x >= self.width:
            return CHARS_COUNT - 1
        if y >= self.height:
            return CHARS_COUNT - 1
        # print "data.length=%s, x=%s, y=%s, (x+y*self.width)=%s" % (len(self.data), x, y, (x+y*self.width))
        return self.data[x + y * self.width]
 
 
def constructHTML():
    '''
    construct html:
    1. write head info (including style)
    2. write every frame image into html
    3. write javascript at the last which is used to animate the frames
    '''
    bmpFiles = os.listdir(TMP_DIR)
 
    f = open('%s/%s' % (OUT_DIR, OUT_HTML_NAME), 'w+')
    f.write(''' <!DOCTYPE>
                <html>
                    <head>
                        <meta charset="utf-8">
                        <style type="text/css">
                            div{
                                font-family: monospace; 
                                font-size: %dpx; 
                                margin: 0 auto;
                            }
                        </style>
                    </head>
                    <body>''' % FONT_SIZE)
 
    print 'convert images (total %d)' % len(bmpFiles)
 
    for i in xrange(len(bmpFiles)):
        bmpPath = '%s/%s' % (TMP_DIR, bmpFiles[i])
        cbmp = CharacterBMP(bmpPath)
 
        print 'converting : %s' % bmpPath
        if i is 0:
            f.write('<div id="%d" style="display:block">' % i)
        else:
            f.write('<div id="%d" style="display:none">' % i)
        f.write(cbmp.toHTML())
        f.write('</div>')
 
    f.write('<audio src="%s" autoplay="autoplay">' % OUT_MP3_NAME)
    f.write(''' <script type="text/javascript">(function() {
                    var FRAME_PER_SECOND = %d;
 
                    var timer = setInterval(anime, 1000 / FRAME_PER_SECOND);
                    var index = 0;
 
                    function anime() {
                        document.getElementById('' + index).style.display = 'none';
                        index++;
                        var next = document.getElementById('' + index);
                        if(!next) {
                            clearInterval(timer);
                            return;
                        } else {
                            next.style.display = 'block';
                            next.innerHTML = next.innerHTML.replace(/ /g, '&nbsp;');
                        }
                    }
            })();</script>''' % RATE)
    f.write('</body></html>')
    f.close()
 
 
if __name__ == '__main__':
    if len(sys.argv) is not 2:
        print 'Usage : python anime.py INPUT_FILE_NAME'
    else:
        filename = sys.argv[1]
 
        # make dirs
        if not os.path.exists(TMP_DIR):
            os.mkdir(TMP_DIR)
        if not os.path.exists(OUT_DIR):
            os.mkdir(OUT_DIR)
        # convert input to mp3
        # os.system('ffmpeg -i %s out/%s' % (filename, OUT_MP3_NAME))
        # convert input to html
        os.system('ffmpeg -i %s -r %d -f image2 tmp/%%05d.bmp' % (filename, RATE))
 
        constructHTML()
 
        # delete temp file and temp dir
        os.system('rm -rf tmp')

# ctxbox
a Python toolbox for CORTEX, the data acquisition system used in the lab.

## The Cortex Image File Format

The following is an excerpt from Section 7 of `DOCS/CtxUser.doc`, from <ftp://helix.nih.gov/lsn/cortex/Older_versions/c596.zip>.

> 7.1.1  The Cortex Image File Format 
> 
> The Cortex image file format  is a binary file, arranged as successive rows of 8 bit pixel values, (i.e. the first horizontal row of pixel values, followed by the second row, etc).  Preceding the image data is a header describing the image file.  Byte location 10-11 should contain the pixel depth of the image.  At byte location 12-13 in the file you should put the X size (i.e., the number of pixels in width), in bytes.  At location 14-15 should be the Y size (i.e., the number of pixels in height).  In addition, at byte location 16-17 should be the number of frames, for movie items.  Subsequent frames of the movie, or standalone image files should just contain a zero in byte 16.  The image data itself should begin at byte location 18 in the file.     

### Bytes Locations in the file.

This is a copy of the Table right below the excerpt.

|  0 - 9 | 10 - 11     | 12 - 13 | 14 - 15 | 16 - 17          | 18 - end   |
|--------|-------------|---------|---------|------------------|------------|
| blank  | Pixel Depth | X size  | Y size  | number of frames | Image data |

#### notes

* 0 - 9 part seems to be called notes, although nobody uses it.
* Pixel Depth always seems to be 8.
* X size is width
* Y size is height
* number of frames is actual number of frames - 1. This means that, for one frame movie, or image, it's 0.
* Image data are `uint8` integers, in C order (row major)
* 
All number in the header (at locations 10-17) are little endian `uint16`.

## TODOS

* [x] add the original CTX format specification somewhere.
* [ ] add LUT specification.

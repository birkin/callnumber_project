#### overview

This is a [django](https://www.djangoproject.com) application that allows staff, via an admin interface, to create customizable categories and associate [Library Of Congress call-number](https://en.wikipedia.org/wiki/Library_of_Congress_Classification) ranges to those categories.

It supports the [Brown Library's](https://library.brown.edu) [NewTitles](https://library.brown.edu/titles/) application, and offers the ability to normalize callnumbers.

---


#### staff usage

- Start at https://apps.library.brown.edu/callnumber/login/
    - You'll be prompted for your Shibboleth login, and, if you're authorized, you'll end up at an admin screen.

- The existing categories are listed alphabetically, along with a display of callnumber ranges associated with each category.

- To edit an entry, click the category name, and you'll then be able to edit the callnumber ranges.
    - Each callnumber range should be separated by a comma, for example: `GF125-GF125.999, HT101-HT395.999` (for `Cities`)
    - Note: when entering callnumber ranges, be sure not to forget the alphabetic prefix before the end of the callnumber range. An _incorrect_ example: `GF125-125.999, HT101-395.999` -- the first range is missing the `GF` before the end-range; the second is missing the `HT` before the end-range.

---


#### api usage

- data dump...
    - v1 (deprecated): https://apps.library.brown.edu/callnumber/v1/?data=dump
    - v2: https://apps.library.brown.edu/callnumber/v2/?data=dump

- callnumber normalization...
    - Multiple callnumbers may be submitted; separate each with a comma.
    - Spaces in callnumbers should be handled fine
    - Example:
        - v1 (deprecated): https://apps.library.brown.edu/callnumber/v1/?callnumber=TP1085,PJ%201001
        - v2: https://apps.library.brown.edu/callnumber/v2/?callnumber=TP1085,PJ%201001

---


#### credits

- The original non-public version of this was written by [Ted Lawless](https://github.com/lawlesst).

- I ([birkin](https://github.com/birkin)) think Ted was inspired by LC normalization code from [Bill Deuber](http://robotlibrarian.billdueber.com). Here's a recent [blog post](http://robotlibrarian.billdueber.com/2014/01/yet-another-lc-callnumber-parser/) by Bill about his [rails gem](https://github.com/billdueber/lc_callnumber) for working with LC callnumbers.

---


#### code contact

[Birkin James Diana](https://github.com/birkin)

---
---


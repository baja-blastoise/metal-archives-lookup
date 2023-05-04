# metal-archives-lookup
A python library for scraping information from the [Metal Archives](https://www.metal-archives.com/) and returning it in formatted text.  Useful for things like IRC or Discord bots.

I would consider this an alpha level release.  Web scraping is an inexact process and the Metal Archives is filled with 20 years of submissions of varying quality.  Please send the search parameters my way if you encounter unexpected results.

## Uses
This library has functions that search for band, artist, or album pages based on name.  It returns formatted text, usually in the form of a table.  I developed this library for use with an IRC or Discord bot.  Each function scrapes a specific URL based on band/album/artist name input.  The functions return information as a string, and can be configured to also output the text straight to the console.  This feature is useful when using the library as part of a bot, so the bot's output can be monitored from the client side.

Each function handles disambiguation by detecting the disambiguation page and returning the options and associated archive number.  Repeating the request with the archive number will provide the final information.

The library provides the following features:
1. **BANDLOOKUP** - Returns general information about the requested band: genre, themes, status, etc.
2. **DISCLOOKUP** - Returns discography for requested band.  Can filter request based on full-length, EP, etc.
3. **MEMBERLOOKUP** - Returns list of band members.  Can filter by current/last known, past, live, etc.
4. **SIMILAR** - Returns similar bands and similarity ranking.
5. **ARTIST** - Returns basic artist info as well as current and past bands.
6. **ALBUMLOOKUP** - Returns track listing and personnel for specified album.

## Installation
Ensure you have the listed dependencies installed, then copy *malookup.py* into your project folder.

## Examples
**BANDLOOKUP**(*band name*, *band number*, *bprint*)

  *band name* - name of target band in string format, can include spaces but should not include special characters.  When in doubt, use the format in the address of the bands page on the archives.

  *band number* - archive number, only necessary for disambiguation purposes, can be left blank otherwise

  *bprint* - True/False, controls whether output is also printed to terminal.  Useful for bot applications.  Defaults to False if unspecified.
    
  ```
  BANDLOOKUP('Bolt Thrower')
  BANDLOOKUP('Bloodbath', 233, True)
  ```

**DISCOGLOOKUP**(*band name*, *band number*, *disctype*, *bprint*)
    
  *disctype* - discography filter: complete, main, live, demo, misc (defaults to main if not entered manually)
    
  ```
  DISCOGLOOKUP('Blood Incantation')
  DISCOGLOOKUP('Wraith', 3540437153, 'complete', True)
  ```
    
**MEMBERLOOKUP**(*band name*, *band number*, *membertype*, *bprint*)
    
  *membertype* - discography filter: current, Last known, Current (live), Past, Past (live), (defaults to Current/Last known if not entered manually)
  
  ```
  MEMBERLOOKUP('Revocation')
  MEMBERLOOKUP('Cannibal Corpse', 0, 'Past', True)
  ```
  
**SIMILAR**(*band name*, *band number*, *bprint*)
  
  ```
  SIMILAR('High on Fire')
  ```
  
**ARTISTLOOKUP**(*artist name*, *artist number*, *bprint*)
  
  ```
  ARTISTLOOKUP('David Davidson',  3493, False)
  ```
  
**ALBUMLOOKUP**(*band name*, *album name*, *album number*, *bprint*)
  
  ```
  ALBUMLOOKUP('Baest', 'Necro Sapiens', 914697, True)
  ```
  
## Dependencies
This library has the following dependencies:
1. **Requests** - Used to scrape text from Metal Archives pages.
2. **Beautiful Soup 4** - Used for some of the web scrape processing.
3. **PrettyTable** - Used to format output into ASCII tables.
4. **textwrap** - keeps output tables within a certain width

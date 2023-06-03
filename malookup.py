import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import textwrap
import sys


def BANDLOOKUP(bandname, bandnumber=0, bprint=0):

    # take input arguments
    bandname = bandname
    bandnumber = bandnumber

    # url will be base_url1 + keyword + baseurl2
    base_url1 = "https://www.metal-archives.com/bands/"
    base_url2 = "/"
    if bandnumber == 0:
        url = base_url1 + bandname + base_url2
    else:
        url = base_url1 + bandname + base_url2 + str(bandnumber)

    # first Metal Archives web scrape
    try:
        # Open the URL as Browser, not as python urllib
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
    except Exception as e:
        if bprint:
            print("Something went wrong - cannot access the Metal Archives")
            print(e)

    b404 = BAND404(page.text, bprint)
    if b404:
        message404 = 'Band not found in the archives.  Try listening to a REAL metal band instead.  Or check your spelling ;)'
        print(message404)
        return message404

    # check for disambiguation page first
    try:
        # search for certain phrases that only appear on disambiguation page
        if page.text.find('may refer to:') != -1:
            # really janky way of finding all the matches, there are probably better ways of doing this
            # this loop just finds the band numbers, need to get the rest of the information; easier from the soup text probably
            options = []
            position = 0
            done = 0
            # replace spaces in URL with '_'
            url = url.replace(' ', '_')
            while done == 0:
                inter_pos = page.text.lower()[position:-1].find(url.lower())
                if inter_pos == -1:
                    done = 1
                    continue
                position = inter_pos + position
                num_start = position + len(url)
                num_end = position + page.text[position:-1].find('"')
                options.append(page.text[num_start:num_end])
                position = position + len(url)
            # options = options[0:-1]
            # find other info
            options_name = []
            options_info = []
            position = 0
            done = 0
            while done == 0:
                inter_pos1 = soup.text.lower(
                )[position:-1].find(bandname.lower() + ' (')
                inter_pos2 = soup.text.lower(
                )[position+inter_pos1:-1].find('\n')
                inter_pos3 = soup.text.lower(
                )[position+inter_pos1+inter_pos2+1:-1].find('\n')
                if inter_pos1 == -1:
                    done = 1
                    continue
                num_start = position + inter_pos1
                num_end = position + inter_pos1 + inter_pos2 + inter_pos3 + 1
                if len(soup.text[num_start:num_end].split('\n')) < 2:
                    continue
                if bprint:
                    print(soup.text[num_start:num_end])
                options_name.append(
                    soup.text[num_start:num_end].split('\n')[0])
                options_info.append(
                    soup.text[num_start:num_end].split('\n')[1])
                position = inter_pos1 + inter_pos2 + inter_pos3 + position
                # options_name = options_name[0:-1]
            disamb_text = "Disambiguation needed.  Please retype request with one of the following band numbers:\n\n"
            # make nice table
            disamb_table = PrettyTable()
            disamb_table.add_column("Name", options_name)
            disamb_table.add_column("Description", options_info)
            disamb_table.add_column("Number", options)
            # spit out results
            disamb_results = disamb_text + disamb_table.get_string()
            if bprint:
                print(disamb_results)
            return disamb_results

    except Exception as e:
        errormsg = "something went wrong - unexpected data"
        if bprint:
            print("Received unexpected results from web scrape")
            print(errormsg)
            print(e)
            print("error on line {}".format(sys.exc_info()[-1].tb_lineno))
        return errormsg

    # if disambiguation page, list options and ask for band number
    # if no disambiguation page, proceed as normal
    try:
        # output band basic details
        # output url scrape for use with other functions
        # BASIC DETAILS
        data = page.text
        details_start = data.find('<div id="band_stats">')
        details_end = details_start + data[details_start:-1].find('</div>')
        details = data[details_start:details_end]

        country_pos = details.find('Country of origin:')
        try:
            country_end = country_pos + details[country_pos:-1].find('</a>')
            country_start = details[country_pos:country_end].split('>')
            COUNTRY = country_start[-1]
            if bprint:
                print(COUNTRY)
        except:
            country_end = country_pos + \
                details[country_pos:-1].find('</a>')[-1]
            country_start = details[country_pos:country_end].split('>')
            COUNTRY = country_start[-1]
            if bprint:
                print(COUNTRY)

        location_pos = details.find('Location:')
        location_start = location_pos + \
            details[location_pos:-1].find('<dd>') + 4
        location_end = location_start + \
            details[location_start:-1].find('</dd>')
        LOCATION = details[location_start:location_end]
        if bprint:
            print(LOCATION)

        status_pos = details.find('Status:')
        status_end = status_pos + details[status_pos:-1].find('</dd>')
        status_start = details[status_pos:status_end].split('>')
        STATUS = status_start[-1]
        if bprint:
            print(STATUS)

        formed_pos = details.find('Formed in:')
        formed_start = formed_pos + details[formed_pos:-1].find('<dd>') + 4
        formed_end = formed_start + details[formed_start:-1].find('</dd>')
        FORMED = details[formed_start:formed_end]
        if bprint:
            print(FORMED)

        genre_pos = details.find('Genre:')
        genre_start = genre_pos + details[genre_pos:-1].find('<dd>') + 4
        genre_end = genre_start + details[genre_start:-1].find('</dd>')
        GENRE = details[genre_start:genre_end]
        if bprint:
            print(GENRE)

        theme_pos = details.find('Themes:')
        theme_start = theme_pos + details[theme_pos:-1].find('<dd>') + 4
        theme_end = theme_start + details[theme_start:-1].find('</dd>')
        THEME = details[theme_start:theme_end]
        if bprint:
            print(THEME)

        label_pos = details.find('label:')
        label_end = label_pos + details[label_pos:-1].find('</dd>')
        label_start = details[label_pos:label_end].split('>')
        LABEL = label_start[-2][0:-3]
        if bprint:
            print(LABEL)

        years_pos = details.find('Years active:')
        years_start = years_pos + details[years_pos:-1].find('<dd>') + 4
        years_end = years_start + details[years_start:-1].find('</dd>')
        YEARS = details[years_start:years_end]
        if YEARS.find('strong') != -1:
            clipstart = YEARS.find('<strong>')
            clipend = YEARS.find('</strong>')
            YEARS = YEARS[0:clipstart] + \
                YEARS[clipstart+8:clipend] + YEARS[clipend+9:-1]
        if YEARS.find('\n') != -1:
            YEARS = YEARS[1:]
        if bprint:
            print(YEARS)
        # reformat multiple years to put them all on one line to make it easier to send IRC message in a single line
        YEARS = YEARS.replace("\n", " ")

        general_info = bandname + ' | ' + COUNTRY + ' | ' + LOCATION + ' | ' + STATUS + \
            ' | ' + FORMED + ' | ' + GENRE + ' | ' + THEME + ' | ' + LABEL + ' | ' + YEARS
        return general_info

    except Exception as e:
        errormsg = "something went wrong - unexpected data"
        if bprint:
            print(errormsg)
            print(e)
            print("error on line {}".format(sys.exc_info()[-1].tb_lineno))
        return errormsg


def DISCOGLOOKUP(bandname, bandnumber=0, disctype='main', bprint=0):

    # take input arguments
    bandname = bandname
    bandnumber = bandnumber

    # url will be base_url1 + keyword + baseurl2
    base_url1 = "https://www.metal-archives.com/bands/"
    base_url2 = "/"
    if bandnumber == 0:
        url = base_url1 + bandname + base_url2
    else:
        url = base_url1 + bandname + base_url2 + str(bandnumber)

    # first Metal Archives web scrape
    try:
        # Open the URL as Browser, not as python urllib
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
    except Exception as e:
        errormsg = "Something went wrong - cannot access the Metal Archives"
        if bprint:
            print(errormsg)
            print(e)
            print("error on line {}".format(sys.exc_info()[-1].tb_lineno))
        return errormsg

    b404 = BAND404(page.text, bprint)
    if b404:
        message404 = 'Band not found in the archives.  Try listening to a REAL metal band instead.  Or check your spelling ;)'
        print(message404)
        return message404

    # check for disambiguation page first
    try:
        if page.text.find('may refer to:') != -1:
            # really janky way of finding all the matches, there are probably better ways of doing this
            # this loop just finds the band numbers, need to get the rest of the information; easier from the soup text probably
            options = []
            position = 0
            done = 0
            # replace spaces in URL with '_'
            url = url.replace(' ', '_')
            while done == 0:
                inter_pos = page.text.lower()[position:-1].find(url.lower())
                if inter_pos == -1:
                    done = 1
                    continue
                position = inter_pos + position
                num_start = position + len(url)
                num_end = position + page.text[position:-1].find('"')
                options.append(page.text[num_start:num_end])
                position = position + len(url)
            # options = options[0:-1]
            # find other info
            options_name = []
            options_info = []
            position = 0
            done = 0
            while done == 0:
                inter_pos1 = soup.text.lower(
                )[position:-1].find(bandname.lower() + ' (')
                inter_pos2 = soup.text.lower(
                )[position+inter_pos1:-1].find('\n')
                inter_pos3 = soup.text.lower(
                )[position+inter_pos1+inter_pos2+1:-1].find('\n')
                if inter_pos1 == -1:
                    done = 1
                    continue
                num_start = position + inter_pos1
                num_end = position + inter_pos1 + inter_pos2 + inter_pos3 + 1
                if len(soup.text[num_start:num_end].split('\n')) < 2:
                    continue
                if bprint:
                    print(soup.text[num_start:num_end])
                options_name.append(
                    soup.text[num_start:num_end].split('\n')[0])
                options_info.append(
                    soup.text[num_start:num_end].split('\n')[1])
                position = inter_pos1 + inter_pos2 + inter_pos3 + position
                # options_name = options_name[0:-1]
            disamb_text = "Disambiguation needed.  Please retype request with one of the following band numbers:\n\n"
            # make nice table
            disamb_table = PrettyTable()
            disamb_table.add_column("Name", options_name)
            disamb_table.add_column("Description", options_info)
            disamb_table.add_column("Number", options)
            # spit out results
            disamb_results = disamb_text + disamb_table.get_string()
            if bprint:
                print(disamb_results)
            return disamb_results

    except Exception as e:
        errormsg = "Received unexpected results from web scrape"
        if bprint:
            print(errormsg)
            print(e)
            print("error on line {}".format(sys.exc_info()[-1].tb_lineno))
        return errormsg

    # get discography information
    # find links
    try:
        data = page.text
        discog_data_start = data.find('id="band_tab_discography"')
        discog_complete_end = discog_data_start + \
            data[discog_data_start:].find('<span>Complete discography')
        discog_main_end = discog_data_start + \
            data[discog_data_start:].find('<span>Main')
        discog_live_end = discog_data_start + \
            data[discog_data_start:].find('<span>Lives')
        discog_demos_end = discog_data_start + \
            data[discog_data_start:].find('<span>Demos')
        discog_misc_end = discog_data_start + \
            data[discog_data_start:].find('<span>Misc.')
    except Exception as e:
        errormsg = "Couldn't find discography links."
        if bprint:
            print(errormsg)
            print(e)
            print("error on line {}".format(sys.exc_info()[-1].tb_lineno))
        return errormsg

    try:
        if disctype == 'complete':
            discog_complete_url_start = discog_data_start + \
                data[discog_data_start:discog_complete_end].find('href=') + 6
            discog_complete_url_end = discog_complete_url_start + \
                data[discog_complete_url_start:discog_complete_end].find(
                    '>') - 1
            page2 = requests.get(
                data[discog_complete_url_start:discog_complete_url_end])

        if disctype == 'main':
            discog_main_url_start = discog_complete_end + \
                data[discog_complete_end:discog_main_end].find('href=') + 6
            discog_main_url_end = discog_main_url_start + \
                data[discog_main_url_start:discog_main_end].find('>') - 1
            page2 = requests.get(
                data[discog_main_url_start:discog_main_url_end])

        if disctype == 'live':
            discog_live_url_start = discog_main_end + \
                data[discog_main_end:discog_live_end].find('href=') + 6
            discog_live_url_end = discog_live_url_start + \
                data[discog_live_url_start:discog_live_end].find('>') - 1
            page2 = requests.get(
                data[discog_live_url_start:discog_live_url_end])

        if disctype == 'demo':
            discog_demos_url_start = discog_live_end + \
                data[discog_live_end:discog_demos_end].find('href=') + 6
            discog_demos_url_end = discog_demos_url_start + \
                data[discog_demos_url_start:discog_demos_end].find('>') - 1
            page2 = requests.get(
                data[discog_demos_url_start:discog_demos_url_end])

        if disctype == 'misc':
            discog_misc_url_start = discog_demos_end + \
                data[discog_demos_end:discog_misc_end].find('href=') + 6
            discog_misc_url_end = discog_misc_url_start + \
                data[discog_misc_url_start:discog_misc_end].find('>') - 1
            page2 = requests.get(
                data[discog_misc_url_start:discog_misc_url_end])

    except Exception as e:
        errormsg = "Failed to scrape discography data."
        if bprint:
            print(errormsg)
            print(e)
            print("error on line {}".format(sys.exc_info()[-1].tb_lineno))
        return errormsg

    # PULL INFO FROM DISCOG SCRAPE
    try:
        NAME = []
        TYPE = []
        YEAR = []
        REVIEW = []
        discog_data = BeautifulSoup(page2.content, "html.parser")
        album_list = discog_data.text.split('\n\n\n')
        for index, x in enumerate(album_list):
            text = album_list[index].strip()
            if len(text) != 0 and text.find('Name\nType\nYear\nReviews') == -1:
                temp_list = text.split('\n')
                NAME.append(temp_list[0])
                TYPE.append(temp_list[1])
                YEAR.append(temp_list[2])
                # fix when album has no reviews
                if len(temp_list) >= 4:
                    REVIEW.append(temp_list[4])
                else:
                    REVIEW.append("no reviews")
        # put results in a table
        disc_table = PrettyTable()
        disc_table.add_column("Name", NAME)
        disc_table.add_column("Type", TYPE)
        disc_table.add_column("Year", YEAR)
        disc_table.add_column("Review Score", REVIEW)
        if bprint:
            print(disc_table)
        return disc_table.get_string()
    except Exception as e:
        errormsg = "Failed formatting table from scrape."
        if bprint:
            print(errormsg)
            print(e)
            print("error on line {}".format(sys.exc_info()[-1].tb_lineno))
        return errormsg


def MEMBERLOOKUP(bandname, bandnumber=0, membertype='Current', bprint=0):

    # take input
    bandname = bandname
    bandnumber = bandnumber

    # url will be base_url1 + keyword + baseurl2
    base_url1 = "https://www.metal-archives.com/bands/"
    base_url2 = "/"
    if bandnumber == 0:
        url = base_url1 + bandname + base_url2
    else:
        url = base_url1 + bandname + base_url2 + str(bandnumber)

    # first scrape
    try:
        # open the URL as a browser, not as python urllib
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
    except Exception as e:
        errormsg = "Something went wrong - cannot access the Metal Archives"
        if bprint:
            print("Something went wrong - cannot access the Metal Archives")
            print(e)
            print("error on line {}".format(sys.exc_info()[-1].tb_lineno))
        return errormsg

    b404 = BAND404(page.text, bprint)
    if b404:
        message404 = 'Band not found in the archives.  Try listening to a REAL metal band instead.  Or check your spelling ;)'
        print(message404)
        return message404

    # check for disambiguation page first
    try:
        # search for certain phrases that only appear on disambiguation page
        if page.text.find('may refer to:') != -1:
            # really janky way of finding all the matches, there are probably better ways of doing this
            # this loop just finds the band numbers, need to get the rest of the information; easier from the soup text probably
            options = []
            position = 0
            done = 0
            # replace spaces in URL with '_'
            url = url.replace(' ', '_')
            while done == 0:
                inter_pos = page.text.lower()[position:-1].find(url.lower())
                if inter_pos == -1:
                    done = 1
                    continue
                position = inter_pos + position
                num_start = position + len(url)
                num_end = position + page.text[position:-1].find('"')
                options.append(page.text[num_start:num_end])
                position = position + len(url)
            # find other info
            options_name = []
            options_info = []
            position = 0
            done = 0
            while done == 0:
                inter_pos1 = soup.text.lower(
                )[position:-1].find(bandname.lower() + ' (')
                inter_pos2 = soup.text.lower(
                )[position+inter_pos1:-1].find('\n')
                inter_pos3 = soup.text.lower(
                )[position+inter_pos1+inter_pos2+1:-1].find('\n')
                if inter_pos1 == -1:
                    done = 1
                    continue
                num_start = position + inter_pos1
                num_end = position + inter_pos1 + inter_pos2 + inter_pos3 + 1
                if len(soup.text[num_start:num_end].split('\n')) < 2:
                    continue
                if bprint:
                    print(soup.text[num_start:num_end])
                options_name.append(
                    soup.text[num_start:num_end].split('\n')[0])
                options_info.append(
                    soup.text[num_start:num_end].split('\n')[1])
                position = inter_pos1 + inter_pos2 + inter_pos3 + position
                # options_name = options_name[0:-1]
            disamb_text = "Disambiguation needed.  Please retype request with one of the following band numbers:\n\n"
            # make nice table
            disamb_table = PrettyTable()
            disamb_table.add_column("Name", options_name)
            disamb_table.add_column("Description", options_info)
            disamb_table.add_column("Number", options)
            # spit out results
            disamb_results = disamb_text + disamb_table.get_string()
            if bprint:
                print(disamb_results)
            return disamb_results

    except Exception as e:
        errormsg = "Received unexpected results from web scrape"
        if bprint:
            print("Received unexpected results from web scrape")
            print(e)
            print("error on line {}".format(sys.exc_info()[-1].tb_lineno))
        return (errormsg)

    # process band members
    try:
        # use this flag to scrap different kinds of member pages (0 is normal)
        member_page_flag = 0
        band_members_raw = soup.find(id="band_tab_members_all")
        # if a band has nevver changed members (wild I know), then the 'all' tab doesn't exist
        if band_members_raw is None:
            band_members_raw = soup.find(id="band_tab_members_current")
            member_page_flag = 1
        band_members = band_members_raw.prettify()

        if member_page_flag == 0:
            section_title = []
            section_start = []
            section_header_start = 0
            while (band_members[section_header_start:-1].find('lineupHeaders') != -1):
                section_header_start = band_members[section_header_start:-1].find(
                    'lineupHeaders') + 51 + section_header_start
                section_header_end = band_members[section_header_start:-1].find(
                    '\n') + section_header_start
                section_title.append(
                    band_members[section_header_start:section_header_end].strip())
                section_start.append(section_header_start)

            member_output = []
            for index, i in enumerate(section_start):
                members = []
                instruments = []
                other_bands = []
                if index < (len(section_start) - 1):
                    lines = band_members[section_start[index]                                         :section_start[index+1]].splitlines()
                else:
                    lines = band_members[section_start[index]:-1].splitlines()
                for jndex, j in enumerate(lines):
                    if lines[jndex].find('<a') != -1:
                        # check to make sure it's not a band in the "See Also" section
                        if lines[jndex].find('artists') != -1:
                            artist_switch = 1  # used to help differentiate between bands and artists in text
                            # check for RIP
                            if (lines[jndex + 3].find('R.I.P.') != -1):
                                member_temp = lines[jndex +
                                                    1].strip() + lines[jndex + 3].strip()
                                members.append(member_temp)
                                instruments.append(lines[jndex + 6].strip())
                            else:
                                members.append(lines[jndex + 1].strip())
                                instruments.append(lines[jndex + 5].strip())
                            other_bands.append('')
                        else:
                            if artist_switch:
                                temp_str = str()
                                temp_index = jndex
                                band_switch = 1
                                while band_switch:
                                    # stop on last line
                                    if temp_index == len(lines) - 1:
                                        band_switch = 0
                                    # found results when looking for html tag
                                    if lines[temp_index].find('<') != -1:
                                        # found next artist line
                                        if lines[temp_index].find('artists') != -1:
                                            band_switch = 0  # stop iterating over lines
                                            continue
                                        else:
                                            temp_index = temp_index + 1
                                            continue
                                    else:
                                        # put it into list
                                        temp_str += lines[temp_index].strip()
                                        temp_index = temp_index + 1
                                other_bands[-1] = textwrap.fill(
                                    temp_str, width=50)
                                artist_switch = 0
                member_output.append(
                    (section_title[index], members, instruments, other_bands))

            return_str = ''
            if membertype.find('all') != -1:
                # print out some tables
                for m in range(0, len(member_output)):
                    member_table = PrettyTable()
                    member_table.add_column("Name", member_output[m][1])
                    member_table.add_column("Instrument", member_output[m][2])
                    member_table.add_column("Other Bands", member_output[m][3])
                    # member_table.align["Other Bands"] = "l"
                    if bprint:
                        print(member_table)
                    return_str += '\n' + membertype + '\n'
                    return_str += member_table.get_string()
                    return_str += '\n'
            else:
                # sort out which table to print
                chosen_member = 0  # should make the first one print, which will either be active or last known depending on band status
                for m in range(0, len(section_title)):
                    if section_title[m].find(membertype) != -1:
                        chosen_member = m
                        # should stop Current from cascading into Current (Live)
                        break
                if bprint:
                    print(chosen_member)
                    print(section_title[chosen_member])
                member_table = PrettyTable()
                member_table.add_column(
                    "Name", member_output[chosen_member][1])
                member_table.add_column(
                    "Instrument", member_output[chosen_member][2])
                member_table.add_column(
                    "Other Bands", member_output[chosen_member][3])
                if bprint:
                    print(member_table)
                return_str += '\n' + membertype + '\n'
                return_str += member_table.get_string()

                notfoundstr = "\nOther possible options: "
                for n in range(0, len(section_title)):
                    notfoundstr += section_title[n]
                    notfoundstr += ','
                return_str += notfoundstr
            return return_str

        elif member_page_flag == 1:
            members = []
            instruments = []
            other_bands = []
            lines = band_members.splitlines()
            artist_switch = 0
            band_switch = 0
            member_output = []
            for jndex, j in enumerate(lines):
                if lines[jndex].find('artists') != -1:
                    artist_switch = 1  # used to help differentiate between bands and artists in text
                    # check for RIP
                    if (lines[jndex + 3].find('R.I.P.') != -1):
                        member_temp = lines[jndex +
                                            1].strip() + lines[jndex + 3].strip()
                        members.append(member_temp)
                        instruments.append(lines[jndex + 6].strip())
                    else:
                        members.append(lines[jndex + 1].strip())
                        instruments.append(lines[jndex + 5].strip())
                    other_bands.append('')
                else:
                    if artist_switch:
                        temp_str = str()
                        temp_index = jndex
                        band_switch = 1
                        while band_switch:
                            if temp_index == len(lines) - 1:  # stop on last line
                                band_switch = 0
                            # found results when looking for html tag
                            if lines[temp_index].find('<') != -1:
                                # found next artist line
                                if lines[temp_index].find('artists') != -1:
                                    band_switch = 0  # stop iterating over lines
                                    continue
                                # found a 'see also' band
                                elif lines[temp_index].find('https://www.metal-archives.com/bands') != -1:
                                    temp_str += lines[temp_index + 1].strip()
                                    temp_index = temp_index + 1
                                else:
                                    temp_index = temp_index + 1
                                    continue
                            else:
                                # put it into list
                                # temp_str += lines[temp_index].strip()
                                temp_index = temp_index + 1
                        other_bands[-1] = textwrap.fill(temp_str, width=50)
                        artist_switch = 0
        member_output.append(('Current', members, instruments, other_bands))
        member_table = PrettyTable()
        member_table.add_column("Name", member_output[0][1])
        member_table.add_column("Instrument", member_output[0][2])
        member_table.add_column("Other Bands", member_output[0][3])
        if bprint:
            print(member_table)
        return_str += '\n' + membertype + '\n'
        return_str + member_table.get_string()
        return return_str

    except Exception as e:
        errormsg = "something went wrong - unexpected data"
        if bprint:
            print(errormsg)
            print(e)
            print("error on line {}".format(sys.exc_info()[-1].tb_lineno))


def SIMILAR(bandname, bandnumber=0, bprint=0):
    # take input arguments
    bandname = bandname
    bandnumber = bandnumber

    # url will be base_url1 + keyword + baseurl2
    base_url1 = "https://www.metal-archives.com/bands/"
    base_url2 = "/"
    if bandnumber == 0:
        url = base_url1 + bandname + base_url2
    else:
        url = base_url1 + bandname + base_url2 + str(bandnumber)

    # first Metal Archives web scrape
    # Open the URL as Browser, not as python urllib
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # first scrape
    try:
        # open the URL as a browser, not as python urllib
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
    except Exception as e:
        errormsg = "Something went wrong - cannot access the Metal Archives"
        if bprint:
            print("Something went wrong - cannot access the Metal Archives")
            print(e)
            print("error on line {}".format(sys.exc_info()[-1].tb_lineno))
        return errormsg

    b404 = BAND404(page.text, bprint)
    if b404:
        message404 = 'Band not found in the archives.  Try listening to a REAL metal band instead.  Or check your spelling ;)'
        print(message404)
        return message404

    # check for disambiguation page first
    try:
        # search for certain phrases that only appear on disambiguation page
        if page.text.find('may refer to:') != -1:
            # really janky way of finding all the matches, there are probably better ways of doing this
            # this loop just finds the band numbers, need to get the rest of the information; easier from the soup text probably
            options = []
            position = 0
            done = 0
            # replace spaces in URL with '_'
            url = url.replace(' ', '_')
            while done == 0:
                inter_pos = page.text.lower()[position:-1].find(url.lower())
                if inter_pos == -1:
                    done = 1
                    continue
                position = inter_pos + position
                num_start = position + len(url)
                num_end = position + page.text[position:-1].find('"')
                options.append(page.text[num_start:num_end])
                position = position + len(url)
            # find other info
            options_name = []
            options_info = []
            position = 0
            done = 0
            while done == 0:
                inter_pos1 = soup.text.lower(
                )[position:-1].find(bandname.lower() + ' (')
                inter_pos2 = soup.text.lower(
                )[position+inter_pos1:-1].find('\n')
                inter_pos3 = soup.text.lower(
                )[position+inter_pos1+inter_pos2+1:-1].find('\n')
                if inter_pos1 == -1:
                    done = 1
                    continue
                num_start = position + inter_pos1
                num_end = position + inter_pos1 + inter_pos2 + inter_pos3 + 1
                if len(soup.text[num_start:num_end].split('\n')) < 2:
                    continue
                if bprint:
                    print(soup.text[num_start:num_end])
                options_name.append(
                    soup.text[num_start:num_end].split('\n')[0])
                options_info.append(
                    soup.text[num_start:num_end].split('\n')[1])
                position = inter_pos1 + inter_pos2 + inter_pos3 + position
                # options_name = options_name[0:-1]
            disamb_text = "Disambiguation needed.  Please retype request with one of the following band numbers:\n\n"
            # make nice table
            disamb_table = PrettyTable()
            disamb_table.add_column("Name", options_name)
            disamb_table.add_column("Description", options_info)
            disamb_table.add_column("Number", options)
            # spit out results
            disamb_results = disamb_text + disamb_table.get_string()
            if bprint:
                print(disamb_results)
            return disamb_results

    except Exception as e:
        errormsg = "Received unexpected results from web scrape"
        if bprint:
            print("Received unexpected results from web scrape")
            print(e)
            print("error on line {}".format(sys.exc_info()[-1].tb_lineno))
        return errormsg

    # related bands
    try:
        related_link_start = page.text.find(
            '"https://www.metal-archives.com/band/ajax-recommendations/') + 1
        related_link_end = page.text[related_link_start:-
                                     1].find('"') + related_link_start
        related_link = page.text[related_link_start:related_link_end+1]

        page2 = requests.get(related_link)
        soup2 = BeautifulSoup(page2.content, "html.parser")

        similar_list = []
        lines = soup2.text.splitlines()
        for i in range(0, len(lines)):
            if len(lines[i]) != 0 and lines[i].find('see more') == -1:
                similar_list.append(lines[i].strip())

        # hacky way to put into table
        num = 4
        similar_mat = [similar_list[i:i+num]
                       for i in range(0, len(similar_list), num)]

        similar_table = PrettyTable()
        similar_table.field_names = similar_mat[0]
        for i in range(1, len(similar_mat)):
            similar_table.add_row(similar_mat[i])

        if bprint:
            print(similar_table)
        return (similar_table.get_string())

    except Exception as e:
        errormsg = "Received unexpected results from web scrape"
        if bprint:
            print("Received unexpected results from web scrape")
            print(e)
            print("error on line {}".format(sys.exc_info()[-1].tb_lineno))
        return errormsg


def ARTISTLOOKUP(artistname, artistnumber=0, bprint=0):
    try:
        # take input arguments
        artistname = artistname
        artistnumber = artistnumber

        # url will be base_url1 + keyword + baseurl2
        base_url1 = "https://www.metal-archives.com/artists/"
        base_url2 = "/"
        if artistnumber == 0:
            url = base_url1 + artistname + base_url2
        else:
            url = base_url1 + artistname + base_url2 + str(artistnumber)

        # first Metal Archives web scrape
        # Open the URL as Browser, not as python urllib
        if bprint:
            print('Scraping URL: ' + url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
    except Exception as e:
        errormsg = "Received unexpected results from web scrape"
        if bprint:
            print("Received unexpected results from web scrape")
            print(e)
            print("error on line {}".format(sys.exc_info()[-1].tb_lineno))
        return errormsg

    # disambiguation
    try:
        (bDisamb, name, location, bands, numbers) = DISAMB_ARTIST(page.text, bprint)
        if bDisamb:
            disamb_str = str()
            disamb_table = PrettyTable()
            disamb_table.add_column("Name", name)
            disamb_table.add_column("From", location)
            disamb_table.add_column("Bands", bands)
            disamb_table.add_column("Numbers", numbers)
            disamb_text = "\nDisambiguation needed.  Please retype request with one of the following artist numbers:\n\n"
            if bprint:
                print(disamb_text)
                print(disamb_table)
            disamb_str += disamb_text
            disamb_str += disamb_table.get_string()
            return disamb_str

    except Exception as e:
        errormsg = "Encountered error in artist disambiguation check"
        if bprint:
            print("Encountered error in artist disambiguation check")
            print(e)
            print("error on line {}".format(sys.exc_info()[-1].tb_lineno))
        return errormsg

    try:
        # find artist info
        realname = str()
        age = str()
        birthplace = str()
        gender = str()
        lines = soup.text.splitlines()

        return_str = str()

        for i in range(0, len(lines)):
            if lines[i].find('Real/full name:') != -1:
                realname = lines[i+2].strip()
            elif lines[i].find('Age:') != -1:
                age = lines[i+1].strip()
            elif lines[i].find('Place of birth:') != -1:
                birthplace = lines[i+1].strip()
            elif lines[i].find('Gender:') != -1:
                gender = lines[i+1].strip()

        if bprint:
            print('Full name: ', realname, ' | Age: ', age,
                  ' | Birthplace: ', birthplace, ' | Gender: ', gender)
        return_str += 'Full name: ' + realname + ' | Age: ' + age + \
            ' | Birthplace: ' + birthplace + ' | Gender: ' + gender

        # find bands
        active = []
        active_role = []
        past = []
        past_role = []
        live = []
        live_role = []
        guest = []
        guest_role = []
        misc = []
        misc_role = []

        # split text up into sections
        active_pos = page.text.find('<div id="artist_tab_active">')
        past_pos = page.text.find('<div id="artist_tab_past">')
        live_pos = page.text.find('<div id="artist_tab_live">')
        guest_pos = page.text.find('<div id="artist_tab_guest">')
        misc_pos = page.text.find('<div id="artist_tab_misc">')

        # active bands
        if active_pos != -1:
            if past_pos == -1 and live_pos != -1:
                chunk = BeautifulSoup(
                    page.text[active_pos:live_pos], "html.parser")
            else:
                chunk = BeautifulSoup(
                    page.text[active_pos:past_pos], "html.parser")
            links = chunk.find_all('h3')
            for i in range(0, len(links)):
                active.append(links[i].text)
            roles = chunk.find_all('p')
            for i in range(0, len(roles)):
                active_role.append(roles[i].text.strip().replace('\n', ' - '))

            x = PrettyTable()
            x.add_column("Band", active)
            x.add_column("Role", active_role)
            if bprint:
                print('\nACTIVE\n')
                print(x)
            return_str += '\nACTIVE\n' + x.get_string()

        # past bands
        if past_pos != -1:
            if live_pos == -1 and guest_pos != -1:
                chunk = BeautifulSoup(
                    page.text[past_pos:guest_pos], "html.parser")
            elif live_pos == -1 and guest_pos == -1 and misc_pos != -1:
                chunk = BeautifulSoup(
                    page.text[past_pos:misc_pos], "html.parser")
            else:
                chunk = BeautifulSoup(
                    page.text[past_pos:live_pos], "html.parser")
            links = chunk.find_all('h3')
            for i in range(0, len(links)):
                past.append(links[i].text)
            roles = chunk.find_all('p')
            for i in range(0, len(roles)):
                past_role.append(roles[i].text.strip().replace('\n', ' - '))

            x = PrettyTable()
            x.add_column("Band", past)
            x.add_column("Role", past_role)
            if bprint:
                print('\nPAST\n')
                print(x)
            return_str += '\nPAST\n' + x.get_string()

        # live bands
        if live_pos != -1:
            chunk = BeautifulSoup(page.text[live_pos:guest_pos], "html.parser")
            links = chunk.find_all('h3')
            for i in range(0, len(links)):
                live.append(links[i].text)
            roles = chunk.find_all('p')
            for i in range(0, len(roles)):
                live_role.append(roles[i].text.strip().replace('\n', ' - '))

            x = PrettyTable()
            x.add_column("Band", live)
            x.add_column("Role", live_role)
            if bprint:
                print('\nLIVE \n')
                print(x)
            return_str += '\nLIVE\n' + x.get_string()

        # will need to be more clever for these, role doesn't have a special formatting

        # # guest bands
        # if guest_pos != -1:
        #     chunk = BeautifulSoup(page.text[guest_pos:misc_pos], "html.parser")
        #     links = chunk.find_all('h3')
        #     for i in range(0, len(links)):
        #         guest.append(links[i].text)
        #     roles = chunk.find_all('p')
        #     for i in range(0, len(roles)):
        #         guest_role.append(roles[i].text.strip().replace('\n',' - '))

        #     x = PrettyTable()
        #     x.add_column("Band", guest)
        #     x.add_column("Role", guest_role)
        #     print(x)

        # # misc bands
        # if misc_pos != -1:
        #     chunk = BeautifulSoup(page.text[misc_pos:-1], "html.parser")
        #     links = chunk.find_all('h3')
        #     for i in range(0, len(links)):
        #         misc.append(links[i].text)
        #     roles = chunk.find_all('p')
        #     for i in range(0, len(roles)):
        #         misc_role.append(roles[i].text.strip().replace('\n',' - '))

        #     x = PrettyTable()
        #     x.add_column("Band", misc)
        #     x.add_column("Role", misc_role)
        #     print(x)

        return return_str
    except Exception as e:
        errormsg = "Received unexpected results from web scrape"
        if bprint:
            print("Something went wrong processing artist results")
            print(e)
            print("error on line {}".format(sys.exc_info()[-1].tb_lineno))
        return errormsg


def DISAMB_ARTIST(raw_text, bprint=0):
    try:
        disamb_pos = raw_text.find('may refer to:')
        if disamb_pos != -1:
            # print formatted options
            chunk = BeautifulSoup(raw_text[disamb_pos:-1], "html.parser")
            groups = chunk.text.split('\n\n')
            name = []
            location = []
            bands = []
            numbers = []
            for i in range(0, len(groups)):
                if len(groups[i]) == 0 or groups[i].find('may refer to:') != -1:
                    continue
                else:
                    option = groups[i].strip().split('\n')
                    if len(option) >= 3:
                        name.append(option[0].strip('-').strip())
                        location.append(textwrap.fill(
                            option[1].strip(), width=50))
                        bands.append(textwrap.fill(
                            option[2].strip(), width=50))
                    # when artist is added but all pands are pending review/removed
                    elif len(option) == 2:
                        name.append(option[0].strip('-').strip())
                        location.append(textwrap.fill(
                            option[1].strip(), width=50))
                        bands.append('')
                    else:
                        name.append(option[0].strip('-').strip())
                        location.append('')
                        bands.append('')
            num_temp = chunk.find_all('a')
            for i in range(0, len(num_temp)):
                link_str = num_temp[i].attrs["href"]
                if link_str.find('artists') != -1:
                    numbers.append(link_str.split('/')[-1].strip())

            return (True, name, location, bands, numbers)
        else:
            return (False, [], [], [], [])

    except Exception as e:
        errormsg = "Something went wrong with artist disambiguation check"
        if bprint:
            print("Something went wrong with artist disambiguation check")
            print(e)
            print("error on line {}".format(sys.exc_info()[-1].tb_lineno))
        return (errormsg)


def DISAMB_ALBUM(raw_text, albumname, bprint=0):
    try:
        disamb_pos = raw_text.find('may refer to:')
        if disamb_pos != -1:
            disamb_name = []
            disamb_number = []
            # print formatted options
            chunk = raw_text[disamb_pos:-1]
            groups = chunk.split('\n')
            for i in range(0, len(groups)):
                if groups[i].find('albums') != -1:
                    disamb_number.append(
                        groups[i].split('"')[1].split('/')[-1])
            chunk2 = BeautifulSoup(chunk, "html.parser")
            groups2 = chunk2.text.split('\n\n')
            for i in range(0, len(groups2)):
                if groups2[i].find(albumname) != -1:
                    disamb_name.append(groups2[i].replace('\n', ' ').strip())
            return (True, disamb_name, disamb_number)
        else:
            return (False, [], [])

    except Exception as e:
        errormsg = "Something went wrong with album disambiguation check (inner)"
        if bprint:
            print("Something went wrong with album disambiguation check (inner)")
            print(e)
            print("error on line {}".format(sys.exc_info()[-1].tb_lineno))
        return (errormsg)


def ALBUMLOOKUP(bandname, albumname, albumnumber=0, bprint=0):
    try:
        # take input arguments
        bandname = bandname
        albumname = albumname
        albumnumber = albumnumber
        if bprint:
            print('Album Name: ' + albumname)
            print('Band Name: ' + bandname)

        return_str = str()

        # url will be base_url1 + keyword + baseurl2
        base_url1 = "https://www.metal-archives.com/albums/"
        base_url2 = "/"
        if albumnumber == 0:
            url = base_url1 + bandname + base_url2 + albumname + base_url2
        else:
            url = base_url1 + bandname + base_url2 + \
                albumname + base_url2 + str(albumnumber)

        # first Metal Archives web scrape
        # Open the URL as Browser, not as python urllib
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        try:
            (bDisamb, option, number) = DISAMB_ALBUM(page.text, albumname, bprint)
            if bDisamb:
                x = PrettyTable()
                x.add_column("Option", option)
                x.add_column("Number", number)
                if bprint:
                    print(x)
                return ('\nDisambiguation needed.\n' + x.get_string())
        except Exception as e:
            errormsg = "Something went wrong with album disambiguation check (outer)"
            if bprint:
                print("Something went wrong with album disambiguation check (outer)")
                print(e)
                print("error on line {}".format(sys.exc_info()[-1].tb_lineno))
            return (errormsg)

        categories = soup.find_all('dt')
        answers = soup.find_all('dd')

        info1 = []
        info2 = []
        for i in range(0, len(categories)):
            info1.append(categories[i].text)
            info2.append(answers[i].text)

        if bprint:
            print(info1[0] + ' ' + info2[0] + ' | ' + info1[1] + ' ' + info2[1] + ' | ' + info1[2] + ' ' +
                  info2[2] + ' | ' + info1[3] + ' ' + info2[3] + ' | ' + info1[4] + ' ' + info2[4] + '\n\n')
        return_str += (info1[0] + ' ' + info2[0] + ' | ' + info1[1] + ' ' + info2[1] + ' | ' + info1[2] +
                       ' ' + info2[2] + ' | ' + info1[3] + ' ' + info2[3] + ' | ' + info1[4] + ' ' + info2[4] + '\n\n')

        track_pos = page.text.find('<div id="album_tabs_tracklist"')
        lineup_pos = page.text.find('<div id="album_tabs_lineup">')
        lineup_end = page.text.find('div id="album_members_lineup"')
        notes_pos = page.text.find('<div id="album_tabs_notes"')

        if track_pos != -1:
            track_chunk = BeautifulSoup(
                page.text[track_pos:lineup_pos], "html.parser")
            dirty_tracks = track_chunk.text.split('\n\n\n')
            clean_tracks = []
            for i in range(0, len(dirty_tracks)):
                clean_tracks.append(dirty_tracks[i].strip())
            track_num = []
            track_name = []
            track_length = []
            for i in range(0, len(clean_tracks)):
                if len(clean_tracks[i]) > 0 and clean_tracks[i].find('loading lyrics...') == -1:
                    data = clean_tracks[i].split('\n\n')
                    if len(data) >= 3:
                        track_num.append(data[0].strip('.').strip())
                        track_name.append(data[1].strip())
                        track_length.append(data[2][0:7].strip())
                    elif len(data) == 2:
                        track_num.append(data[0].strip('.').strip())
                        track_name.append(data[1].strip())
                        track_length.append('')
                    else:
                        track_num.append('')
                        track_name.append('')
                        track_length.append('')
            track_table = PrettyTable()
            track_table.add_column("Track", track_num)
            track_table.add_column("Name", track_name)
            track_table.add_column("Length", track_length)
            if bprint:
                print('\n\nTRACK LISTING\n\n')
                print(track_table)
            return_str += '\n\nTRACK LISTING\n\n'
            return_str += track_table.get_string()

        if lineup_pos != -1:
            lineup_chunk = BeautifulSoup(
                page.text[lineup_pos:lineup_end], "html.parser")
            dirty_lineup = lineup_chunk.text.split('\n\n\n')
            clean_lineup = []
            for i in range(0, len(dirty_lineup)):
                if len(dirty_lineup[i]) > 1 and dirty_lineup[i].find('Complete lineup') == -1:
                    clean_lineup.append(dirty_lineup[i].strip())

            band_member_pos = -1
            guest_pos = -1
            misc_pos = -1
            if bprint:
                print(band_member_pos)
                print(guest_pos)
                print(misc_pos)
            for i in range(0, len(clean_lineup)):
                if clean_lineup[i].find('Band members') != -1:
                    band_member_pos = i
                if clean_lineup[i].find('Guest') != -1:
                    guest_pos = i
                if clean_lineup[i].find('Miscellaneous') != -1:
                    misc_pos = i

            band_name = []
            band_lineup = []
            if band_member_pos != -1:
                if guest_pos != -1:
                    band = clean_lineup[band_member_pos:guest_pos]
                elif band_member_pos != -1 and misc_pos != -1:
                    band = clean_lineup[band_member_pos:misc_pos]
                else:
                    band = clean_lineup[band_member_pos:-1]
                # check for weird spacing, might be related to RIP?
                for i in range(1, len(band)):
                    if band[i].find('\n\n') != -1:
                        band.insert(i+1, band[i].split('\n\n')[-1])
                        band[i] = band[i].split('\n\n')[0]
                for i in range(1, len(band)):
                    if i % 2:
                        band_name.append(band[i].strip())
                    else:
                        band_lineup.append(band[i].strip())

                band_table = PrettyTable()
                band_table.add_column("Name", band_name)
                band_table.add_column("Position", band_lineup)
                if bprint:
                    print('\n\nBAND LINEUP\n')
                    print(band_table)
                return_str += '\n\nBAND LINEUP\n'
                return_str += band_table.get_string()

            guest_name = []
            guest_lineup = []
            if guest_pos != -1 and misc_pos != -1:
                guest = clean_lineup[guest_pos:misc_pos]
                # check for weird spacing, might be related to RIP?
                for i in range(1, len(guest)):
                    if guest[i].find('\n\n') != -1:
                        guest.insert(i+1, guest[i].split('\n\n')[-1])
                        guest[i] = guest[i].split('\n\n')[0]
                for i in range(1, len(guest)):
                    if i % 2:
                        guest_name.append(guest[i].strip())
                    else:
                        guest_lineup.append(guest[i].strip())

                guest_table = PrettyTable()
                guest_table.add_column("Name", guest_name)
                guest_table.add_column("Position", guest_lineup)
                if bprint:
                    print('\n\nGUEST SESSION\n')
                    print(guest_table)
                return_str += '\n\nGUEST SESSION\n'
                return_str += guest_table.get_string()

            misc_name = []
            misc_lineup = []
            if misc_pos != -1:
                misc = clean_lineup[misc_pos:]
                # check for weird spacing, might be related to RIP?
                for i in range(1, len(misc)):
                    if misc[i].find('\n\n') != -1:
                        misc.insert(i+1, misc[i].split('\n\n')[-1])
                        misc[i] = misc[i].split('\n\n')[0]
                for i in range(1, len(misc)):
                    if i % 2:
                        misc_name.append(misc[i].strip())
                    else:
                        misc_lineup.append(misc[i].strip())

                misc_table = PrettyTable()
                misc_table.add_column("Name", misc_name)
                misc_table.add_column("Position", misc_lineup)
                if bprint:
                    print('\n\nMISCELLANEOUS STAFF\n')
                    print(misc_table)
                return_str += '\n\nMISCELLANEOUS STAFF\n'
                return_str += misc_table.get_string()
        return return_str
    except Exception as e:
        errormsg = "Something went wrong processing album results"
        if bprint:
            print("Something went wrong processing album results")
            print(e)
            print("error on line {}".format(sys.exc_info()[-1].tb_lineno))
        return (errormsg)


def BAND404(raw_text, bprint=0):
    if raw_text.find('Band not found') != -1:
        return True
    else:
        return False
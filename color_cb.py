import itertools
import os
import re
import sys

try:
    from skimage.color import deltaE_ciede2000, rgb2lab
    # check that you have the right libraries for fancy color distance
except ImportError:
    print('----WARNING----- use  pip install scikit-image to use deltaE color difference\n')


def name_to_tag_dict(abs_path_to_file):
    # read the countries file and create a TAG dict from the file
    new_dict = {}
    with open(abs_path_to_file) as f:
        for line in f:
            match = re.search(r"([A-Z]{3})(.*/)(.*)(.txt)", line)
            if match:
                groups = match.groups()
                new_dict[groups[2]] = groups[0]
    return new_dict


def country_color_dict(abs_path_to_folder):
    # read the first 300 characters of all the files in the countries folder and look for colors
    country_dict = {}
    for file in os.listdir(abs_path_to_folder):
        if file.endswith('.txt'):
            with open(os.path.join(abs_path_to_folder, file)) as f:
                data = f.read()[:300]
                try:
                    country_dict[file[:-4]] = [int(x) for x in
                                               re.search(r"(\d+)(\s+)(\d+)(\s+)(\d+)", data).groups()[::2]]
                except AttributeError:
                    print(file)
                except Exception as e:
                    print(e, 'Help me help you @fannypiggs')
                    input('press enter to quit')
                    quit()
    return country_dict


def color_calculation(rgb1, rgb2, mode='euclidean'):
    # simple euclidean and CIELAB color calculation
    distance = 0
    if mode == 'euclidean':
        distance = ((rgb1[0] - rgb2[0]) ** 2 + (rgb1[1] - rgb2[1]) ** 2 + (rgb1[2] - rgb2[2]) ** 2) ** .5
    elif mode == 'deltaE':
        try:
            lab1 = rgb2lab([[rgb1]])
            lab2 = rgb2lab([[rgb2]])
            distance = deltaE_ciede2000(lab1, lab2)
        except ImportError:
            print('----WARNING----- use  pip install scikit-image to use deltaE color difference\n')
    return distance


def main():
    if not os.path.exists('eu4.exe'):  # check that the file is in the same folder as Eu4.exe
        print('This needs to be in the same directory as eu4.exe in order to find your files')
        input('press enter to quit')
        quit()
    distance = 10
    mode = 'euclidean'

    # check your arguments to make sure they work
    if len(sys.argv) == 2:
        try:
            float(sys.argv[1])
        except ValueError:
            distance = 10
            if sys.argv[1] == 'euclidean' or sys.argv[1] == 'deltaE':
                mode = sys.argv[1]
            else:
                print('Unable to parse the mode: use euclidean or deltaE')
                input('press enter to quit')
                quit()
        except Exception as e:
            print(e, 'Help me help you @fannypiggs')
            input('press enter to quit')
            quit()
        else:
            distance = float(sys.argv[1])
            mode = 'euclidean'
    elif len(sys.argv) == 3:
        try:
            distance = float(sys.argv[1])
            mode = sys.argv[2]
        except ValueError:
            print('Put in order distance -> mode')
            input('press enter to quit')
            quit()
        except Exception as e:
            print(e, 'Help me help you @fannypiggs')
            input('press enter to quit')
            quit()

    # find the files

    file_path = r'''common\country_tags\00_countries.txt'''
    my_path = r'''common\countries'''

    if mode == 'euclidean':
        print('Expected to complete max run in .9229472s')
    if mode == 'deltaE':
        print('Expected to complete max run in 121.83914159999999s')
    # start the correct mode

    color_dict = country_color_dict(my_path)
    tag_dict = name_to_tag_dict(file_path)

    # read mod folders
    mod_folders = os.listdir(os.path.abspath(os.getcwd()) + '\\mod')
    for x in mod_folders:
        if os.path.isdir(os.path.abspath(os.getcwd()) + '\\mod' + '\\' + x):
            common_folder = os.path.join(os.path.abspath(os.getcwd()) + '\\mod' + '\\' + x, my_path)
            country_file = os.listdir(os.path.abspath(os.getcwd()) + '\\mod' + '\\' + x + r'\common\country_tags')[0]
            countries_tags = os.path.join(os.path.abspath(os.getcwd()) + '\\mod' + '\\' + x + r'\common\country_tags',
                                          country_file)
            color_dict = {**color_dict, **country_color_dict(common_folder)}
            tag_dict = {**tag_dict, **name_to_tag_dict(countries_tags)}
    country_list = color_dict.keys()
    all_pairs = list(itertools.combinations(country_list, 2))
    # create a list of all possible country matches thanks itertools

    cb_dict = {}
    failures = 0
    matches = 0
    fail_list = ['Biapis', 'Limbdi', 'Morang', 'Nsenga']  # No Tag in file
    fail_list += ['BritishWestAfrica', 'BritishIndia', 'BritishSouthAfrica', 'BritishWestAfrica', 'BritishSouthAfrica',
                  'BritishEastIndies', 'BritishPhilippines'] #No Tag in file
    for pair in all_pairs:
        if color_calculation(color_dict[pair[0]], color_dict[pair[1]], mode=mode) < distance:
            try:
                if tag_dict[pair[0]] not in cb_dict.keys():
                    cb_dict[tag_dict[pair[0]]] = [tag_dict[pair[1]]]
                else:
                    cb_dict[tag_dict[pair[0]]].append(tag_dict[pair[1]])
                matches += 1
            except KeyError:
                failures += 1
                if pair[0] not in fail_list and pair[1] not in fail_list:
                    print('Failed to match the follwowing pairs', pair[0], pair[1])

    # write the file here
    with open('color_cb.csv', 'w+') as outfile:
        for key in cb_dict.keys():
            outfile.write(key + ',' + ','.join(cb_dict[key]) + '\n')

    # report out
    print("21 failures expected at max distance. {} failures caught. ".format(failures + len(fail_list)))
    print("{} countries would gain CBs based upon their color similaritiy".format(len(set(cb_dict.keys()))))
    print("{} cbs were given out".format(matches))
    print('File written to {}\color_cb.csv'.format(os.path.abspath(os.getcwd()), 'color_cb.csv'))


if __name__ == '__main__':
    main()
=======
import itertools
import os
import re
import sys

try:
    from skimage.color import deltaE_ciede2000, rgb2lab
    # check that you have the right libraries for fancy color distance
except ImportError:
    print('----WARNING----- use  pip install scikit-image to use deltaE color difference\n')


def name_to_tag_dict(abs_path_to_file):
    # read the countries file and create a TAG dict from the file
    new_dict = {}
    with open(abs_path_to_file) as f:
        for line in f:
            match = re.search(r"([A-Z]{3})(.*/)(.*)(.txt)", line)
            if match:
                groups = match.groups()
                new_dict[groups[2]] = groups[0]
    return new_dict


def country_color_dict(abs_path_to_folder):
    # read the first 300 characters of all the files in the countries folder and look for colors
    country_dict = {}
    for file in os.listdir(abs_path_to_folder):
        if file.endswith('.txt'):
            with open(os.path.join(abs_path_to_folder, file)) as f:
                data = f.read()[:300]
                try:
                    country_dict[file[:-4]] = [int(x) for x in
                                               re.search(r"(\d+)(\s+)(\d+)(\s+)(\d+)", data).groups()[::2]]
                except AttributeError:
                    print(file)
                except Exception as e:
                    print(e, 'Help me help you @fannypiggs')
                    input('press enter to quit')
                    quit()
    return country_dict


def color_calculation(rgb1, rgb2, mode='euclidean'):
    # simple euclidean and CIELAB color calculation
    distance = 0
    if mode == 'euclidean':
        distance = ((rgb1[0] - rgb2[0]) ** 2 + (rgb1[1] - rgb2[1]) ** 2 + (rgb1[2] - rgb2[2]) ** 2) ** .5
    elif mode == 'deltaE':
        try:
            lab1 = rgb2lab([[rgb1]])
            lab2 = rgb2lab([[rgb2]])
            distance = deltaE_ciede2000(lab1, lab2)
        except ImportError:
            print('----WARNING----- use  pip install scikit-image to use deltaE color difference\n')
    return distance


def main():
    if not os.path.exists('eu4.exe'):  # check that the file is in the same folder as Eu4.exe
        print('This needs to be in the same directory as eu4.exe in order to find your files')
        input('press enter to quit')
        quit()
    distance = 10
    mode = 'euclidean'

    # check your arguments to make sure they work
    if len(sys.argv) == 2:
        try:
            float(sys.argv[1])
        except ValueError:
            distance = 10
            if sys.argv[1] == 'euclidean' or sys.argv[1] == 'deltaE':
                mode = sys.argv[1]
            else:
                print('Unable to parse the mode: use euclidean or deltaE')
                input('press enter to quit')
                quit()
        except Exception as e:
            print(e, 'Help me help you @fannypiggs')
            input('press enter to quit')
            quit()
        else:
            distance = float(sys.argv[1])
            mode = 'euclidean'
    elif len(sys.argv) == 3:
        try:
            distance = float(sys.argv[1])
            mode = sys.argv[2]
        except ValueError:
            print('Put in order distance -> mode')
            input('press enter to quit')
            quit()
        except Exception as e:
            print(e, 'Help me help you @fannypiggs')
            input('press enter to quit')
            quit()

    # find the files

    file_path = r'''common\country_tags\00_countries.txt'''
    my_path = r'''common\countries'''

    if mode == 'euclidean':
        print('Expected to complete max run in .9229472s')
    if mode == 'deltaE':
        print('Expected to complete max run in 121.83914159999999s')
    # start the correct mode

    color_dict = country_color_dict(my_path)
    country_list = color_dict.keys()
    tag_dict = name_to_tag_dict(file_path)
    all_pairs = list(itertools.combinations(country_list, 2))
    # create a list of all possible country matches thanks itertools

    cb_dict = {}
    failures = 0
    matches = 0
    fail_list = ['Biapis', 'Limbdi', 'Morang', 'Nsenga']  # Cmon Paradox
    for pair in all_pairs:
        if color_calculation(color_dict[pair[0]], color_dict[pair[1]], mode=mode) < distance:
            try:
                if tag_dict[pair[0]] not in cb_dict.keys():
                    cb_dict[tag_dict[pair[0]]] = [tag_dict[pair[1]]]
                else:
                    cb_dict[tag_dict[pair[0]]].append(tag_dict[pair[1]])
                matches += 1
            except KeyError:
                failures += 1
                if pair[0] not in fail_list and pair[1] not in fail_list:
                    print(pair[0], pair[1])

    # write the file here
    with open('color_cb.csv', 'w+') as outfile:
        for key in cb_dict.keys():
            outfile.write(key + ',' + ','.join(cb_dict[key]) + '\n')

    # report out
    print("3202 failures expected at max distance. {} failures caught. ".format(failures))
    print("{} countries would gain CBs based upon their color similaritiy".format(len(set(cb_dict.keys()))))
    print("{} cbs were given out".format(matches))
    print('File written to {}\color_cb.csv'.format(os.path.abspath(os.getcwd()), 'color_cb.csv'))


if __name__ == '__main__':
    main()
>>>>>>> origin/master

# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 10:56:13 2021

@author: lyuch
"""

# Your name:lyuch
# Your student id:62850933
# Your email:lyuch@umich.edu
# List who you have worked with on this homework:

import unittest
import os


class FileReader:
    """
    Represents a generic file reader. Used to read in data from a file of the
    user’s choice, analyze, and manipulate its data as Python objects.
    """
    def __init__(self, filename):
        """
        The constructor. Creates a new FileReader object based on the
        specified filename. For our purposes, the file should be in the same
        folder as HW5.py. To open a file called “mydiary.txt”, you would call
        FileReader(‘mydiary.txt’)
        """

        # this gives you the full path to the folder that this HW5.py is in
        # using the os library allows the code to run on Mac or Windows
        self.root_path = os.path.dirname(os.path.abspath(__file__))

        # all we have to do now is add the name of the file we want to open
        # to the full path
        self.filename = os.path.join(self.root_path, filename+".csv")

    def open_file(self):
        """
        Opens the file in read only mode, stores the resulting object as an
        instance variable called file_obj.
        """

        self.file_obj = open(self.filename, 'r', errors='replace', encoding = 'utf-8-sig')

    def read_lines(self):
        """
        Reads the lines from the file object into a list where each row of the
        CSV is a seperate element and stores it as an instance variable called
        file_data. Then closes the file object.
        """

        self.file_data = self.file_obj.readlines()
        self.file_obj.close()

    def strip_trailing_newlines(self):
        """
        Removes unnecessary newline characters (\n) from the end of
        each string in file_data.
        """

        for i in range(len(self.file_data)):
            self.file_data[i] = self.file_data[i].replace('\n', '')


class CsvReader(FileReader):
    """
    A child class of FileReader for reading CSV files only.
    """

    def __init__(self, csvfile):
        """
        The constructor. Overwrites the FileReader constructor such that in
        order to read a file called “mycsv.csv”, one only needs to call
        CsvReader(‘mycsv’). (Since CsvReader is designed to work only with
        .csv files, we don’t need to specify an extension.)
        """

        super().__init__(csvfile)

    def build_data_dict(self):
        """
        Accesses the data stored in the file_data instance variable (a list)
        and converts it to a dictionary, data_dict, where each key is a column
        name found in the CSV, and each value is a list of data in that column
        with the same order as it was in the file.  Each element of the list
        corresponds to a single row in the CSV. For example, to access the 
        “Title” column in the CSV, I would access data_dict[‘Title’].
        """

        self.data_dict = {
            'Title': [],
            'Pages': [],
            'URL': [],
            'Author Name': [],
            'Genre': [],
        }

        for i in self.file_data[1:]:
            row = i.split(',')
            self.data_dict['Title'].append(row[0])
            self.data_dict['Pages'].append(row[1])
            self.data_dict['URL'].append(row[2])
            self.data_dict['Author Name'].append(row[3])
            self.data_dict['Genre'].append(row[4])

    def get_title_pages(self):
        """
        From the data stored in the data_dict instance variable, returns a
        list of tuples containing the title of the book and its pages (as an integer) in the
        format (Title, Pages). The list should be sorted based on descending order of pages.
        For example, [('Gone with the Wind', 1037), ('The Book Thief’, 552), ('Fahrenheit 451', 194)]
        """
        sorted_tuples = []
        tuples_list = []
        for i in range(len(self.data_dict['Title'])):
            tuples_list.append(
                (self.data_dict['Title'][i], int(self.data_dict['Pages'][i]))
                )

        sorted_tuples = sorted(tuples_list, key=lambda x: x[1], reverse=True)

        return sorted_tuples

    def get_genre_counts(self):
        """
        From the data stored in the data_dict instance variable, returns a
        list of tuples in the format ('Fantasy', 10) where the
        first element is the genre, and the second element is the number of
        books with that genre. The list should be sorted in descending order
        by the number of books.
        For example, [(‘Fantasy’, 20), (‘Horror’, 15), (‘Science Fiction’, 12), (‘Romance’, 8)]
        """
        sorted_genre_counts={}
        genre_counts = {}
        for genre in self.data_dict['Genre']:
            genre_counts[genre] = genre_counts.get(genre, 0) + 1
        sorted_genre_counts = sorted(genre_counts.items(),key = lambda item: item[1], reverse=True)
        return sorted_genre_counts


    def most_common_length(self):
        """
        Iterates through the "Pages" column and counts the number of books that 
        were in the same hundred pages length (less than or equal to 100 pages, 
        more than 100 and less than 200, etc).  Finally, returns the length with 
        the most number of books. For example, given page numbers: ['432', '422', '254', 156'], 
        this method would return 400.
        """

        length_counts = {}
        for i in self.data_dict['Pages']:
            hundred_pages = int(str(i)[:-2])
            length_counts[hundred_pages] = length_counts.get(hundred_pages, 0)+1

        top_length = sorted(length_counts.items(),key = lambda item: item[1], reverse=True)

        return int(str(top_length[0][0])+ "00")

    def get_book_ID(self):
        """
        Returns a list of IDs for each row in the 'URL' column of the CSV by extracting 
        the ID from the end of the URL. (i.e. the ID that would be extracted from the 
        URL"https://www.goodreads.com/book/show/7624" would be "7624") 
        For example, given:  [‘https://www.goodreads.com/book/show/7624’, 
        ‘https://www.goodreads.com/book/show/19063’, ‘https://www.goodreads.com/book/show/2657’], 
        this method would return ['7624', '19063', '2657'].
        """

        ids = []
        for i in self.data_dict['URL']:
            ids.append(int((i.split('show/'))[1]))
        return ids

    # If you are attempting the extra credit, you can define
    # find_common_first_initial below
    def find_common_first_initial(self):
        """
        Returns a list of tuples, with each tuple consisting of two elements. 
        The first element should be a common first initial, i.e. the first 
        character of the author’s first name shared by more than 1 book. The second 
        element should indicate the number of books that share that first initial. Finally, 
        this list should be sorted in decreasing order of the number of books.
        For example, this method should return a list like: 
        [('L', 5), ('S', 3), ('T', 2)]
        """
        m=[]
        k={}
        for i in self.data_dict['Author Name']:
            k[i[0]]=k.get(i[0],0)+1
            
        for l in k.items():
            if(l[1]>1):
              m.append(l)
        m=sorted(m,key = lambda item: item[1], reverse=True)
        return m
        


##############################################################################
# DO NOT MODIFY ANY CODE BELOW THIS - These are the test cases you must pass
##############################################################################

class TestHomework5(unittest.TestCase):
    def setUp(self):
        try:
            self.reader = CsvReader('HW5Data')
            self.reader.open_file()
        except FileNotFoundError:
            self.reader = CsvReader('HW5Data.csv')
            self.reader.open_file()
        self.reader.read_lines()
        self.reader.strip_trailing_newlines()
        self.reader.build_data_dict()

    def test_constructor(self):
        reader2 = CsvReader('testing123')
        self.assertTrue(reader2.filename.endswith('testing123.csv'))

    def test_read_lines(self):
        self.assertTrue(self.reader.file_obj.closed)

    def test_newline_strip(self):
        self.assertEqual(
            self.reader.file_data[0],
            'Title,Pages,URL,Author Name,Genre'
            )

    def test_first_row(self):
        self.assertEqual(self.reader.data_dict['Title'][0], 'The Book Thief')
        self.assertEqual(self.reader.data_dict['Pages'][0], '552')
        self.assertEqual(
            self.reader.data_dict['URL'][0],
            'https://www.goodreads.com/book/show/19063'
            )
        self.assertEqual(self.reader.data_dict['Author Name'][0], 'Markus Zusak')
        self.assertEqual(self.reader.data_dict['Genre'][0], 'Historical Fiction')

    def test_get_title_pages(self):
        target = [
            ('Gone with the Wind', 1037),
            ('The Chronicles of Narnia', 767),
            ('The Book Thief', 552)
            ]
        self.assertEqual(self.reader.get_title_pages()[:3], target)

    def test_get_genre_counts(self):
        expected = [
            ('Historical Fiction', 5),
            ('Science Fiction', 4),
            ('Romance', 2),
            ('Fantasy', 2),
            ('Philosophy', 1),
            ('Mystery Thriller', 1),
            ('Horror', 1)
            ]
        self.assertEqual(self.reader.get_genre_counts(), expected)

    def test_most_common_length(self):
        self.assertEqual(type(self.reader.most_common_length()), int)
        self.assertEqual(self.reader.most_common_length(), 300)

    ###########################################################################
    # You may modify the test case below.
    # You are required to write 2 assert statements in a loop here.
    # This is not extra credit.
    ###########################################################################

    def test_get_book_ID(self):
        """
        Write the test case for get_book_ID. You should loop over the data returned 
        by CsvReader.test_get_book_ID( ) and write two assert statements within that 
        loop. The first assert statement should test if each ID starts with a number. 
        The second should check whether the length of each ID is at least 3.  
        We will check that your output for CsvReader.get_book_ID() passes a hidden 
        test case that meets the above two requirements. You will receive points for 
        passing our version of this test case, and correctly implementing (and passing) 
        your own version of this test case.
        """

       

    
        ids = self.reader.get_book_ID()
        for i in ids:
           self.assertEqual(type(i), int)
           self.assertEqual((len(str(i))>=3), True)
        
        pass
 

    ###########################################################################
    # If you are doing the extra credit, write your new test case below.
    ###########################################################################
    def test_find_common_first_initial(self):
        idt=self.reader.find_common_first_initial()
        
        m=idt[0][1]
        
        for i in idt:
         self.assertEqual((i[1]>1),True)
         self.assertEqual((i[1]<=m),True)
         m=i[1]
         pass

# Provided main() runs the above test cases
def main():
    unittest.main(verbosity=2)

# Standard boilerplate to call the main() function that tests all your code
if __name__ == '__main__':
    main()
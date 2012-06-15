Readme

Current Efforts on XML Parsing:

Files Modified:

Parse.py
XMLPatent.py


Testing Harnesses Created:

Test_XML_Patent.py (to test XMLPatent.py), currently runs on multiple xml fixtures
Test_SQL_Patent.py (to test SQLPatent.py), currently only runs on a single xml fixture

-----------------------------------------------------

Initial Discovery: 

  Some of the XML files would return an error if it was ran through parse.py. 
Through reverse engineering, it was apparent that there are a few edge cases that the original 
code did not account for. Hence, the regex would not be able to pull separate XMLs out of the 
containing XML file, because these edge cases had different ending tags. For example, a general patent,
which the code worked for, had a starting tag <?xml ... > and an ending tag </us-patent-grant>, and
the regex in parse.py accurately grabs these general patents and calls XMLPatent.py to deconstruct them.
However, an edge patent had different ending tags such as </sequence-cwu>, so the regex would incorrectly
grab xmls if edge patents were present in the file. 

  Furthermore, even if the regex problem was fixed to account for these edge patents, they would still raise
an error in XMLPatent.py, because some of these patents had missing fields, notably elements under the tag
<application-reference>. XMLPatent.py would then try to get the children elements of <application-reference>
only to find out it doesn't exist and return an error. Quick solution: First check if that tag exists, if so, 
get the children elements. If not, set the corresponding parsed field to be empty (ex. self.date_app = ""). 

Testing Harnesses:

  For Test_XML_Patent.py, the tests are separated into three levels: high, medium, and low level tests. The high-level
test just tests the construction of the patent using XMLPatent.py. If it fails there, it will definitely fail all the 
other tests, following a fail-fast mentality. The medium-level tests checks the logic of the fields. For example,
patents cannot be referenced before July 31st, 1790, the first patent ever granted. Date fields should have numbers,
and Country fields should have letters, as well as be two characters long. Kind fields should be in the set of 
valid kind types (see the code or the paper for the list), etc... The low level tests checks for the XML presence of the
field that XMLPatent.py deconstructed from the original xml. For example, if self.date_app is 19901207, there must be
the tags <application-reference>...<date>19901207</date>...</application-reference>. Test_XML_Patent.py does this 
for almost all of the xml field data deconstructed in XMLPatent.py. 

For Test_SQL_Patent.py, the only method tested is tblBuild(), and the tests in the harness check that the list of lists is
correctly constructed, by checking each call to tblBuild separately (Ex. checked if tbl=assignee, tbl=citation, etc...)


-----------------------------------------------------

Things still needed to be done:

  The regex in parse.py needs to be updated to account for the general patent plus any edge cases. Since there are a large
number of xml files, and each file itself is quite large (~300-400MB), this needs to be implemented both efficiently and
accurately. 

  In Test_XML_Patent.py, some of the fields don't test correctly, and some of those issues may stem from an encoding issue,
some fields have HTML 4.0 "Special Entities" (For example, some fields may be encoded, like Johnson &#38; Johnson. Here, 
"&#38;" is a HTML4.0 Special Entity that renders a "&" that needs to be dealt with in the field checking).
Possible solution here called "Beautiful Soup": http://www.crummy.com/software/BeautifulSoup/

  In Test_SQL_Patent.py, need to finish testing the other methods other than tblBuild(), implement logging
  
  Continue documentation for edge cases (start tag, end tag, extra or missing fields) 
  
Current edge cases:
1. Dna-related sequences, start tag: <?xml ...>, ending tag: </sequence-cwu>

Comments and Suggestions:

There may be many more edge cases. If one exists, follow these steps to get to work correctly. 
1. Set up regex to grab them from the xml file
2. Set up XMLPatent.py to make sure that the right fields are being stored

What makes an unusual and uncommon tag? A general patent (the far majority of most patents), has a starting tag <?xml...> 
and ending tag: </us-patent-grant>. By contrast, a edge patent (uncommon, unusual) does not satisfy both of the above. 
Usually, the end tag will be different. Furthermore, edge patents may have different (extra or missing) fields. 

How do you find unusual and uncommon tags? Easiest way: Run it through parse.py, if there is a parsing error, 
it is likely that there is an edge patent not being considered. 
Hardest way: Manually examine the heading/ending tags for each xml in the file. 

  

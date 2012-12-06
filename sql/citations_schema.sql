/**
 *
Schema Description
------------------------

Patent:      8 character alphanumeric identification assigned by the USTPO
Citation:    Grant number for cited patent.
Cit_Date:    Grant date of cited patent. As of 2012/12/06, the date value
             stored in the database may be reassign the day to the first of
             each month rather than the day upon which the cited patent
             was granted. For example, patent 6,000,000 cites patent 4,432,057
             granted on February 14, 1984. We're storing the grant date as
             February 1, 1984.
Cit_Name:    Primary inventor last name on cited patent.
Cit_Kind:    Patent kind codes (defined in Appendix 2) cited by defined patent
             Many empty fields, candidate for removal from schema.
Cit_Country: Not documented. Many fields are empty. Good candidate for
             removal from schema.
Category:    Cited source of patent (Cited by examiner, other).
             Apparently not widely stored, good candidate for removal
             from schema.
citseq:      Position of cited patent in sequence (0 = first citation).
             Apparently not widely stored. Good candidate for removal
             from schema.
*/

/**
 * Citations in the SQLite3 files are
 * split. This table covers years 2000
 * through 2010. Schemas for other years
 * are identical.
 */
CREATE TABLE citation00_10 (
  Patent      VARCHAR(8),
  Cit_Date    INTEGER,
  Cit_Name    VARCHAR(10),
  Cit_Kind    VARCHAR(1),
  Cit_Country VARCHAR(2),
  Citation    VARCHAR(8),
  Category    VARCHAR(15),
<<<<<<< HEAD
  CitSeq      INTEGER
);
=======
  CitSeq      INTEGER);
>>>>>>> cleaned up formatting for easier reading


CREATE UNIQUE INDEX idx_idx1 ON citation00_10 (patent,citation);
CREATE INDEX idx_idx2 ON citation00_10 (citation);
CREATE INDEX idx_idx3 ON citation00_10 (patent);

-- Example USPTO XML citation fragment
/**
 *
The development of patents is oftentimes based on research from previous
patents, known simply as a citation.  Within the USPTO XML file,
citations are organized numerically through a patent citation number reference.
The document number mimics the format that constitutes the previously
mentioned patent number and type.  Here we are able to determine that
this patent’s first citation is to design patent #20662 and its 38th
citation is to design patent #540507.

<references-cited>
  <citation>
    <patcit num="00001">
      <document-id>
                ……
        <doc-number>D20662</doc-number>
                ……
      </document-id>
    </patcit>
        ……
  </citation>
    ……
  <citation>
    <patcit num="00038">
      <document-id>
                ……
        <doc-number>D540507</doc-number>
                ……
      </document-id>
    </patcit>
        ……
  </citation>
</references-cited>


*/


# Historical source search and access log

Date: 29 September 2026. All reads were scoped to the Paper U review. This log records evidence levels explicitly: a catalog entry, indexed text, OCR, and a visually inspected page are different kinds of evidence.

## Searches

The following public-web queries were issued:

1. `"The Unconscious as an Ultrametric Set" pdf`
2. `"Matte Blanco" "Unconscious as Infinite Sets" preview`
3. `"The Unconscious as Infinite Sets" "38" "39"`
4. `"The Unconscious as Infinite Sets" site:books.google.com`
5. `"The Unconscious as Infinite Sets" preview 107`
6. `"The Unconscious as Infinite Sets" 9780429483899` (mistyped DOI/ISBN suffix; did not support any conclusion)
7. `"lauro-grotto_american-imago.pdf"`
8. `"Lauro-Grotto" "Ultrametric" filetype:pdf`
9. `"Matte Blanco" "The Unconscious as Infinite Sets" "preview" "38"`

Search results from unverified document mirrors were not used. Secondary accounts were not substituted for primary-page verification.

## Authoritative source locations and actual access

| Source | URL | Access result and use |
|---|---|---|
| Routledge book record | https://www.routledge.com/The-Unconscious-as-Infinite-Sets-An-Essay-in-Bi-logic/MatteBlanco/p/book/9781855752023 | Search-indexed publisher record available; direct web open errored. Bibliographic discovery only. |
| Publisher preview | https://api.pageplace.de/preview/DT0400.9780429908361_A35173827/preview-9780429908361_A35173827.pdf | Downloaded from authorized public preview; 51 PDF pages. Title/copyright and printed pp.16-17 rendered locally with Poppler and visually inspected. Requested later pages are absent from this PDF. |
| Google Books 1998 catalog | https://books.google.com/books/about/The_Unconscious_as_Infinite_Sets.html?id=RxI-zAEACAAJ | Linked to later limited-preview editions; catalog not treated as text evidence. |
| Authorized Routledge Google Books preview | https://books.google.com/books?id=GmEPEAAAQBAJ | Web-fetch tool failed, but ordinary in-app browser displayed publisher-authorized page images. Actual browser redirected to books.google.co.id. No login, purchase, or CAPTCHA was required for these pages. |
| Taylor & Francis book page | https://www.taylorfrancis.com/books/mono/10.4324/9780429483592/unconscious-infinite-sets-ignacio-matte-blanco | 403 Forbidden in web tool; not evidence for substantive claims. |
| Florence repository record | https://flore.unifi.it/handle/2158/373430 | Web-indexed record accessible; identifies author and open-access deposited manuscript. Live browser blocked by automatic security challenge. |
| Florence deposited article | https://flore.unifi.it/bitstream/2158/373430/1/lauro-grotto_american-imago.pdf | Indexed text accessible, including p.537. Direct web fetch failed. Initial PowerShell request failed authentication/TLS; escalated ordinary request returned 403. No PDF downloaded. |
| Florence current file link | https://flore.unifi.it/retrieve/e398c378-b25c-179a-e053-3705fe0a4cff/lauro-grotto_american-imago.pdf | Link observed on repository record. Direct web request failed; authorized shell request returned anti-bot challenge. No challenge bypassed. |
| Lauro-Grotto author upload | https://www.researchgate.net/publication/236697092_The_Unconscious_as_an_Ultrametric_Set | Indexed full article text with printed page headers accessible and inspected. Page explicitly identifies full text as author-uploaded. Live browser showed DataDome device check; not solved. |
| Author-upload PDF link | https://www.researchgate.net/publication/profile/Rosapia-Lauro-Grotto/publication/236697092_The_Unconscious_as_an_Ultrametric_Set/links/00b7d5277c01fe3e5f000000/The-Unconscious-as-an-Ultrametric-Set.pdf | Observed from author-upload page; web fetch failed. No PDF image verification claimed. |
| Article DOI | https://doi.org/10.1353/aim.2008.0009 | Web request inaccessible. DOI corroborated by author upload and institutional record. |
| Journal issue record | https://www.jstor.org/stable/i26303511 | Search-indexed issue record identifies volume 64(4), Winter 2007, article pages 535-543. Used only for issue-date discrepancy. |

## Reproducing the successful primary-page inspection

Open the Google Books preview in a normal browser. Navigate to the following URLs and inspect the actual printed page number on each image. The viewport may initially show a loading placeholder; only the completed image was counted. Scroll down to read the lower half and adjacent page; the page label changes during scrolling. Preview availability can change by date or location.

| Direct starting URL | Pages visually inspected | Extent |
|---|---|---|
| https://books.google.com/books?id=GmEPEAAAQBAJ&pg=PA38 | 38-39 | Both principles on 38; succession and part/whole/member treatment on 39. |
| https://books.google.com/books?id=GmEPEAAAQBAJ&pg=PA45 | 45-46; continuation at top of 47 | Relevant passages through lower 46, then continuation into 47. |
| https://books.google.com/books?id=GmEPEAAAQBAJ&pg=PA107 | 107-108 | Both pages, including the translation/unfolding naming and observer-knowledge distinction. |
| https://books.google.com/books?id=GmEPEAAAQBAJ&pg=PA146 | 146-149 | Sequential upper/lower page inspection, including the end of 149. |
| https://books.google.com/books?id=GmEPEAAAQBAJ&printsec=copyright | iv | Publication years/publishers, separate foreword copyright, printed ISBN. |

The browser sidebar visibly states that the pages are displayed with Routledge permission. Some neighboring off-target page containers temporarily displayed an unavailable-page notice while loading. None of the ten cited pages was certified from such a notice; all had readable images inspected in the session.

Google Books asset export was attempted once for already displayed pp.38-39. The browser security check was unavailable, so access to the asset export was not granted. No page images were downloaded from Google Books, no access control was bypassed, and no claim of persistent local image evidence is made. The visible screenshots remain in the task's tool transcript; this log is the portable evidence record.

## Downloaded publisher preview metadata

Local inspection file: `evidence/matte_blanco_publisher_preview.pdf`.

SHA-256: `D731C59BE968BECA7D2A34148A83520EF1C4F77FC98CF6E25E58F1C440284C2C`.

Page offsets are **one-based physical PDF pages**:

- PDF page 4: title leaf, author and Eric Rayner foreword attribution.
- PDF page 5: copyright/publication leaf, ISBN 9781855752023.
- PDF pages 47-48: printed pages 16-17.

Web extraction used zero-based PDF indices internally, so its P46 corresponds to physical PDF page 47. No offset for later cited pages can be inferred from this truncated PDF: those pages were inspected in Google Books by their visible printed numbers.

The preview was rendered using `pdftoppm -f 4 -l 5 -scale-to 1500 -png` and `pdftoppm -f 47 -l 48 -scale-to 1500 -png`. Poppler returned two bad-annotation-destination warnings for the latter command but rendered the pages; these warnings did not concern text content. A first attempt to render through PyMuPDF failed because that package was absent; Poppler was already available and used successfully.

## Packaging and residual limits

Exclude `historical_review/evidence/` source PDF/PNG files from the complete handoff ZIP; distribute these markdown findings and links. No large quoted passages are needed for the argument. The original Internet Archive OCR locator remains part of historical input provenance but was not used for this fresh certification.

No primary-page request to the user remains necessary for the bounded manuscript. Original-edition variant collation and a new image-level check of Lauro-Grotto remain unperformed; neither should be implied by a source-fidelity pass for the modest retained claims.

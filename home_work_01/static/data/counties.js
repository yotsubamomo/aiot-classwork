/* Taiwan Map county names for the Now mode's county interaction layer (Issue #38,
 * SPEC-V2 R-V2-DD-1, R-V2-DD-4). Project-authored data; do not reorder.
 *
 * Loaded as a same-origin <script> that sets window.TAIWAN_COUNTY_NAMES; the
 * browser makes NO request for it and it holds no URL and no key (INV-V2-3).
 *
 * Entry i is the CWA `CountyName` (verbatim, 「臺」 not 「台」) of polygon i of the
 * vendored basemap's `taiwan` layer (window.TAIWAN_BASEMAP.taiwan.geometries[i],
 * static/data/basemap.js — the MOI 直轄市、縣市界線 open-data polygons, Open
 * Government Data License). The app joins the two into the county interaction
 * layer: 22 polygons, each carrying its county name, used only as interaction
 * geometry (hover, click), never coloured by data. The basemap itself is
 * unchanged and stays a non-interactive backdrop (DR-20 P-2(c)).
 *
 * The join is checked offline (tests/test_county_frontend.py): the 22 names are
 * exactly the 22 counties, each once, and every polygon holds a majority of the
 * committed sample's valid stations of the county named here.
 */
window.TAIWAN_COUNTY_NAMES = Object.freeze([
  "連江縣", "宜蘭縣", "彰化縣", "南投縣", "雲林縣", "屏東縣", "基隆市", "臺北市",
  "新北市", "臺南市", "桃園市", "嘉義市", "嘉義縣", "金門縣", "高雄市", "臺東縣",
  "花蓮縣", "澎湖縣", "新竹市", "臺中市", "苗栗縣", "新竹縣"
]);

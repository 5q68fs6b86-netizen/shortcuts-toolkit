# Shortcuts Actions Reference

Complete catalog of all 427 WF*Action classes and their identifiers.

## Identifier Mapping Rules

### Standard Mapping
Class `WF<Name>Action` maps to `is.workflow.actions.<lowercasename>`
Example: `WFShowResultAction` → `is.workflow.actions.showresult`

### Irregular Mappings

| Class Name | Identifier |
|------------|-----------|
| `WFRepeatAction` | `is.workflow.actions.repeat.count` |
| `WFForEachRepeatAction` | `is.workflow.actions.repeat.each` |
| `WFFiniteRepeatAction` | `is.workflow.actions.repeat.count` |
| `WFAskForInputAction` | `is.workflow.actions.ask` |
| `WFTextAction` | `is.workflow.actions.gettext` |
| `WFConditionalAction` | `is.workflow.actions.conditional` |
| `WFChooseFromMenuAction` | `is.workflow.actions.choosefrommenu` |
| `WFGetFileAction` | `is.workflow.actions.documentpicker.open` |
| `WFSelectFilesAction` | `is.workflow.actions.documentpicker.open` |
| `WFSaveFileAction` | `is.workflow.actions.documentpicker.save` |
| `WFGetCurrentWeatherConditionsAction` | `is.workflow.actions.weather.currentconditions` |
| `WFGetWeatherForecastAction` | `is.workflow.actions.weather.forecast` |
| `WFContentItemFilterAction` | `is.workflow.actions.filter.contentitems` |
| `WFGetUpcomingCalendarItemsAction` | `is.workflow.actions.getupcomingevents` |
| `WFAppendFileAction` | `is.workflow.actions.file.append` (was `appendfile`) |

---

## Actions by Category

### Text & Input
| Identifier | Class | Description |
|------------|-------|-------------|
| `gettext` | WFTextAction | Create a text value |
| `ask` | WFAskForInputAction | Ask user for input |
| `askllm` | WFAskLLMAction | Use AI model (Apple Intelligence) |
| `comment` | WFCommentAction | Add a comment (no effect) |
| `dictatetext` | WFDictateTextAction | Dictate text |
| `showresult` | WFShowResultAction | Display result to user |
| `alert` | WFAlertAction | Show alert dialog |
| `notification` | WFNotificationAction | Send notification |
| `speaktext` | WFSpeakTextAction | Speak text aloud |
| `translatetext` | WFTranslateTextAction | Translate text |
| `detectlanguage` | WFDetectLanguageAction | Detect language |

### Variables
| Identifier | Class | Description |
|------------|-------|-------------|
| `setvariable` | WFSetVariableAction | Set a variable |
| `getvariable` | WFGetVariableAction | Get a variable |
| `appendvariable` | WFAppendVariableAction | Append to variable |
| `nothing` | WFNothingAction | Do nothing (pass-through) |

### Control Flow
| Identifier | Class | Description |
|------------|-------|-------------|
| `repeat.count` | WFRepeatAction | Repeat N times |
| `repeat.each` | WFForEachRepeatAction | Repeat for each item |
| `conditional` | WFConditionalAction | If/Otherwise |
| `choosefrommenu` | WFChooseFromMenuAction | Menu with cases |
| `choosefromlist` | WFChooseFromListAction | Choose from list |
| `exit` | WFExitAction | Exit shortcut |
| `output` | WFOutputAction | Set output |

### Files & Documents
`file`, `documentpicker.open`, `documentpicker.save`, `getfoldercontents`, `createfolder`, `deletefile`, `movefile`, `renamefile`, `file.append` (was appendfile), `makearchive`, `extractarchive`

### Web & URLs
`url`, `downloadurl`, `openurl`, `expandurl`, `geturlheaders`, `urlgetcomponent`, `urlencode`, `getwebpage`, `searchweb`

### Apps & System
`openapp`, `quitapp`, `hideapp`, `getcurrentapp`, `runworkflow`, `runshellscript`, `runosascript`, `getdevicedetails`, `batterylevel`, `getclipboard`, `setclipboard`

### Lists & Data
`list`, `dictionary`, `getdictionaryvalue`, `setdictionaryvalue`, `getitemfromlist`, `count`, `filter.contentitems`

### Numbers & Math
`number`, `calculate`, `calculatestatistics`, `randomnumber`, `roundnumber`, `measurementcreate`, `measurementconvert`

### Date & Time
`date`, `formatdate`, `adjustdate`, `converttimezone`, `timeuntildate`, `delay`, `waittoreturn`

### Calendar & Reminders
`addnewevent`, `getupcomingevents`, `removecalendaritems`, `addnewreminder`, `showreminderslist`

### Weather & Location
`weather.currentconditions`, `weather.forecast`, `getcurrentlocation`, `location`, `getdirections`, `getdistance`, `searchmaps`

### Media
`takephoto`, `takevideo`, `selectphoto`, `getlatestphotos`, `filter.photos`, `savetocameraroll`, `deletephotos` (**uses `photos` param, not `WFInput`**), `playmusic`, `playpause`, `skipsong`, `recordaudio`, `playsound`

### Images
`imageresize`, `imagecrop`, `imagerotate`, `imageflip`, `imageconvert`, `imagecombine`, `overlayimage`, `overlaytext`, `imageremovebackground`, `maskimage`, `extracttextfromimage` (OCR)

### PDF
`makepdf`, `splitpdf`, `compresspdf`, `gettextfrompdf`, `makeimagefrompdfpage`

### Sharing & Communication
`share`, `airdrop`, `sendmessage`, `sendemail`, `startcall`, `contacts`, `selectcontacts`

### Settings
`setappearance`, `setwifi`, `setcellulardata`, `setlowpowermode`, `setvolume`, `toggledonotdisturb`, `setorientationlock`, `setwallpaper`

---

## Complete Identifier List (prefix `is.workflow.actions.` omitted)

```
addframetogif, addmusictoupnext, addnewcalendar, addnewcontact, addnewevent,
addnewreminder, addquickreminder, address, addtoplaylist, addtoreadinglist,
adjustdate, airdrop, alert, appattributed, appenddropboxfile, file.append,
appendtonote, appendvariable, appintentexecution, ask, askllm, batterylevel,
calculate, calculateexpression, calculatestatistics, changeplaybackdestination,
choosefromlist, choosefrommenu, clearupnext, coercion, comment, compactdialog,
compresspdf, conditional, configuredactionbuttonintent, configuredactionbuttonnothing,
configuredactionbuttonworkflow, configuredstaccato, configuredstaccatointent,
configuredstaccatonothing, configuredstaccatotophit, configuredstaccatoworkflow,
configuredsystem, configuredsystemcontrol, configuredsystemintent,
configuredsystemnothing, configuredsystemworkflow, connecttoservers, contacts,
contentattributionsetdebugger, contentitem, contentitemproperties, contentitemsetter,
controlflow, converttimezone, count, createfolder, createnote, createphotoalbum,
createplaylist, date, delay, deletefile, deletephotos, detectlanguage, dictatetext,
dictionary, displaysleep, documentpicker.open, documentpicker.save, downloadurl,
ejectdisk, emailaddress, encodemedia, evernoteappend, evernotecreate, evernotedelete,
evernotegetlink, evernotegetnotes, exit, expandurl, extractarchive,
extracttextfromimage, file, filter.contentitems, finderimageconvert,
findhealthsamples, focusconfigurationlink, folder, formatdate, formatfilesize,
formatnumber, generatehash, generatemachinereadablecode, getclass, getclipboard,
getcurrentapp, getcurrentlocation, getcurrentsafariwebpage, getcurrentsong,
getdevicedetails, getdictionaryvalue, getdirections, getdistance, getdropboxfile,
getemojiname, getepisodesforpodcast, getfilelink, getfocus, getfoldercontents,
getframesfromimage, gethalfwaypoint, gethomeaccessorystate, gethotspotpassword,
getipaddress, getitemfromlist, getitemname, getitemtype, getlatestphotoimport,
getlatestphotos, getmapslink, getmyworkflows, getnetworkdetails, getonscreencontent,
getparentdirectory, getparkedcarlocation, getplaylist, getpodcastsfromlibrary,
getposters, getselectedfinderfiles, gettext, gettextfrompdf, gettraveltime,
gettype, getupcomingevents, geturlheaders, getvariable, getwebpage, giphy,
handlecustomintent, handledonatedintent, handleintent, handlepaymentintent,
handlesystemintent, handoff, handoffplayback, hideapp, homeaccessory,
htmlfromrichtext, imagecombine, imageconvert, imagecrop, imageflip,
imageremovebackground, imageresize, imagerotate, imgurupload, importaudiofiles,
importtolightroom, input, instapaper, instapaperadd, instapaperget, interchange,
interchangescheme, intercom, labelfiles, link, linkactionserializedparametersforln,
linkbookschangepagenavigation, linkbookschangetheme, linkbooksfind,
linkbooksnavigatepages, linkcalculateappusageintent, linkcalendarclosescreen,
linkcalendarcreatecalendar, linkcalendardeletecalendar, linkcalendaropenscreen,
linkchangebinarysetting, linkclockcreatealarm, linkclockdeletealarm,
linkclocktogglealarm, linkcloseentity, linkcontentitemfilter, linkcopyentity,
linkcreateentity, linkdeleteentity, linkentity, linkfavoriteentity, linkfindhome,
linkfindhomecameraclip, linkfindhomedevice, linkfindhomeroom, linkfindhomescene,
linkfindhomezone, linkfindselectedhome, linkimageplaygroundgenerateimage,
linkinsertintelligencetext, linkipdatafindsportsevents,
linkmusicrecognitionrecognizemusic, linknavigatesequentially,
linknotesaddtagstonotes, linknoteschangesetting, linknotescreatefolder,
linknotescreatetag, linknotesdeletefolders, linknotesdeletetags, linknotesfind,
linknotesmovenotestofolder, linknotesopenaccount, linknotesopenapplocation,
linknotesopenfolder, linknotesopentag, linknotespinnotes,
linknotesremovetagsfromnotes, linkopencamera, linkopenentity,
linkphotoscreatememory, linkreminderscreatelist, linkremindersopensmartlist,
linkrunintelligencecommand, linksafarichangereadermodestate, linksafariclosetab,
linksafaricreateprivatetab, linksafaricreatetab, linksafaricreatetabgroup,
linksafarifindbookmarks, linksafarifindreadinglistitems, linksafarifindtabgroups,
linksafarifindtabs, linksafariopenbookmark, linksafariopenreadinglistitem,
linksafariopentab, linksafariopentabgroup, linksafariopenview, linksearch,
linkshortcutscreateicloudlink, linkshortcutscreateworkflow,
linkshortcutsdeleteworkflow, linkshortcutsresetcellulardatastatistics,
linkshortcutssearchshortcuts, linkshortcutssetdataroaming, linkshortcutssetdefaultline,
linkshortcutstogglecellularplan, linkstartstopwatch, linkstartworkout,
linktogglehomeaccessory, linkvisualintelligencecamera,
linkvoicememoschangerecordingplaybacksetting, linkvoicememoscreatefolder,
linkvoicememosdeletefolders, linkvoicememosdeleterecordings, linkvoicememosopenfolder,
linkvoicememosopenrecording, linkvoicememosplayrecording, linkvoicememosrecordingfind,
linkvoicememossearchrecordings, linkwritingtools, linkwritingtoolsadjusttone,
linkwritingtoolsformatlist, linkwritingtoolsformattable, linkwritingtoolsproofread,
linkwritingtoolsrewrite, linkwritingtoolssummarize, list, location, lockapp,
lockscreen, loghealthsample, logoutuser, logworkout, makearchive, makediskimage,
makegif, makeimagefrompdfpage, makeimagefromrichtext, makepdf,
makespokenaudiofromtext, makevideofromgif, markdownfromrichtext, markup, maskimage,
measurementconvert, measurementcreate, missing, mountdiskimage, movefile, movewindow,
nothing, notification, number, openapp, openin, openincalendar, openurl,
openuseractivity, openxcallbackurl, output, overlayimage, overlaytext,
overridablelink, phonenumber, pinboardadd, pinboardget, playmusic, playpause,
playpodcast, playsound, pocketadd, pocketget, print, quicklook, quitapp,
randomnumber, recognizemusic, recordaudio, remoteappintentexecution, remotelink,
removecalendaritems, removephotofromalbum, renamefile, repeat.count, repeat.each,
replacetext, requestrideintent, requestuber, resizewindow, returntohomescreen,
revealfiles, reversiblelink, richtextfromhtml, richtextfrommarkdown, roundnumber,
rssfeed, rssfeedextract, runjavascriptonwebpage, runosascript, runshellscript,
runshortcutconfigurationintent, runshortcutintent, runsshscript, runworkflow,
savedropboxfile, savetocameraroll, scanmachinereadablecode, searchitunes,
searchlocalbusinesses, searchmaps, searchweb, seek, selectcontacts, selectmusic,
selectphoto, sendemail, sendmessage, sendtogoodreader, setairdropreceiving,
setalwaysondisplay, setappearance, setcellulardata, setclipboard, setdictionaryvalue,
sethotspotpassword, setitemname, setlisteningmode, setlowpowermode, setorientationlock,
setparkedcar, setvariable, setvolume, setvpn, setwallpaper, setwifi, share,
shareextension, shazammedia, showdefinition, showinblindsquare, showinstore, shownote,
showpasswords, showreminderslist, showresult, showwebpage, shutdowndevice, skipsong,
sleepdevice, social, speaktext, splitpdf, splitscreenapp, spotlightsearch,
staccatolink, standaloneshortcut, startcall, startscreensaver, starttimer,
storageservice, storageserviceinput, subscribetopodcast, switchposter, takephoto,
takescreenshot, takevideo, textcomponents, timeuntildate, todoistadd,
toggledonotdisturb, translatetext, trelloaddcard, trellocreateboard, trellocreatelist,
trellogetitems, trimvideo, trimwhitespace, tumblrpost, ulyssesattach, url, urlencode,
urlgetcomponent, vibrate, viewcontentgraph, waittoreturn, watchmedo,
weather.currentconditions, weather.forecast, wordpresspost
```

---

## Common Parameter Patterns

### Text
```xml
<key>WFTextActionText</key><string>Your text here</string>
```
### Boolean
```xml
<key>WFSomeOption</key><true/>
```
### Number / Enum
```xml
<key>WFRepeatCount</key><integer>5</integer>
<key>WFHTTPMethod</key><string>GET</string>
```

### Variable Reference
```xml
<key>Text</key>
<dict>
    <key>Value</key><dict>
        <key>attachmentsByRange</key><dict>
            <key>{0, 1}</key><dict>
                <key>OutputUUID</key><string>SOURCE-UUID</string>
                <key>OutputName</key><string>Text</string>
                <key>Type</key><string>ActionOutput</string>
            </dict>
        </dict>
        <key>string</key><string>￼</string>
    </dict>
    <key>WFSerializationType</key><string>WFTextTokenString</string>
</dict>
```

---

## Get Contents of URL (`downloadurl`)

| Parameter | Type | Description |
|-----------|------|-------------|
| `UUID` | String | Unique identifier |
| `WFURL` | Variable ref or string | The URL |
| `WFHTTPMethod` | String | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| `WFHTTPBodyType` | String | `JSON`, `Form`, `File` |
| `WFHTTPHeaders` | WFDictionaryFieldValue | Headers (key-value items) |
| `WFJSONValues` | WFDictionaryFieldValue | When body=JSON |
| `WFFormValues` | WFDictionaryFieldValue | When body=Form |
| `WFRequestVariable` | variable ref | When body=File |

`WFItemType`: 0=Text, 1=Number, 2=Array, 3=Dictionary, 4=Boolean

## Find Photos (`filter.photos`)

| Parameter | Description |
|-----------|-------------|
| `WFContentItemFilter` | Filter conditions (see FILTERS.md) |
| `WFContentItemSortProperty` | `Date Taken`, `Creation Date`, ... |
| `WFContentItemSortOrder` | `Latest First` / `Oldest First` |
| `WFContentItemLimitEnabled` | Boolean |
| `WFContentItemLimitNumber` | Integer |

## Delete Photos (`deletephotos`) — ⚠️ uses `photos`, NOT `WFInput`

> 来源：openclaw/skills · shortcuts-skill (erik-agens)。本地缓存于 reference/。

# Content Item Filters Reference

Documentation for `WFContentItemFilter` used in Find/Filter actions like FindPhotos, FindFiles, FindReminders, etc.

## Filter Structure

```xml
<key>WFContentItemFilter</key>
<dict>
    <key>Value</key>
    <dict>
        <key>WFActionParameterFilterPrefix</key><integer>1</integer>
        <key>WFContentPredicateBoundedDate</key><false/>
        <key>WFActionParameterFilterTemplates</key>
        <array><!-- Filter conditions --></array>
    </dict>
    <key>WFSerializationType</key>
    <string>WFContentPredicateTableTemplate</string>
</dict>
```

## Operator Reference

| Operator | Meaning |
|----------|---------|
| 3 | `>=` greater than or equal |
| 4 | `is` exact match |
| 5 | `is not` not equal |
| 8 | `begins with` |
| 9 | `ends with` |
| 99 | `contains` |
| 100 | `has any value` not empty |
| 101 | `does not have any value` is empty |
| 999 | `does not contain` |
| 1000 | `is in the next` future date range |
| 1001 | `is in the last` past date range |
| 1002 | `is today` date is today |
| 1003 | `is between` date range |

## Unit Reference

### Date Units (operators 1000, 1001)
| Unit | Meaning |
|------|---------|
| 4 | years |
| 8 | months |
| 8192 | weeks |

### Boolean/Enum Unit
| Unit | Context |
|------|---------|
| 4 | Standard unit for boolean and enumeration |

## Filter Templates by Type

### Boolean Filter (e.g., Is a Screenshot)
```xml
<dict>
    <key>Operator</key><integer>4</integer>
    <key>Property</key><string>Is a Screenshot</string>
    <key>Removable</key><true/>
    <key>Values</key><dict><key>Bool</key><true/><key>Unit</key><integer>4</integer></dict>
</dict>
```

### "Is Today" Date Filter (operator 1002, NO Values needed)
```xml
<dict>
    <key>Operator</key><integer>1002</integer>
    <key>Property</key><string>Date Taken</string>
    <key>Removable</key><true/>
</dict>
```

### "Is in the Last X" (operator 1001, needs Number + Unit)
```xml
<dict>
    <key>Operator</key><integer>1001</integer>
    <key>Property</key><string>Date Taken</string>
    <key>Removable</key><true/>
    <key>Values</key><dict><key>Number</key><integer>1</integer><key>Unit</key><integer>8192</integer></dict>
</dict>
```

### Enumeration Filter (e.g., Media Type — only Image/Video/Live Photo)
```xml
<dict>
    <key>Operator</key><integer>4</integer>
    <key>Property</key><string>Media Type</string>
    <key>Removable</key><true/>
    <key>Values</key><dict>
        <key>Unit</key><integer>4</integer>
        <key>Enumeration</key><dict>
            <key>Value</key><string>Image</string>
            <key>WFSerializationType</key><string>WFStringSubstitutableState</string>
        </dict>
    </dict>
</dict>
```

### String Filter (e.g., Album name)
```xml
<dict>
    <key>Operator</key><integer>4</integer>
    <key>Property</key><string>Album</string>
    <key>Removable</key><true/>
    <key>Values</key><dict><key>String</key><string>Favorites</string><key>Unit</key><integer>4</integer></dict>
</dict>
```

## Available Filter Properties by Content Type

### Photos
`Album`(enum), `Media Type`(enum: Image/Video/Live Photo), `Is a Screenshot`(bool), `Is Hidden`(bool), `Is Favorite`(bool), `Date Taken`(date), `Creation Date`(date), `Width`(num), `Height`(num), `Orientation`(enum), `Photo Type`(enum), `Frame Rate`(num), `Duration`(num), `Camera Make`(str), `Camera Model`(str), `File Extension`(str)

### Files
`Name`(str), `File Extension`(str), `Creation Date`(date), `File Size`(num), `Last Modified Date`(date)

### Reminders
`Title`(str), `Is Completed`(bool), `Priority`(enum: None/Low/Medium/High), `Due Date`(date), `Creation Date`(date), `List`(enum)

## DeletePhotos（⚠️ 关键）

DeletePhotos 用参数 `photos`（小写），**不是** `WFInput`：

```xml
<dict>
    <key>WFWorkflowActionIdentifier</key><string>is.workflow.actions.deletephotos</string>
    <key>WFWorkflowActionParameters</key>
    <dict>
        <key>UUID</key><string>DELETE-UUID</string>
        <key>photos</key>
        <dict>
            <key>Value</key>
            <dict>
                <key>OutputName</key><string>Photos</string>
                <key>OutputUUID</key><string>FIND-PHOTOS-UUID</string>
                <key>Type</key><string>ActionOutput</string>
            </dict>
            <key>WFSerializationType</key><string>WFTextTokenAttachment</string>
        </dict>
    </dict>
</dict>
```

## Common Mistakes

1. Using `Media Type="Screenshot"` — WRONG, use `Is a Screenshot` boolean
2. Using Operator 4 for "is today" — WRONG, use 1002
3. Using `WFInput` for DeletePhotos — WRONG, use `photos`
4. Adding Values to "is today" filter — WRONG, 1002 needs none
5. Forgetting OutputUUID reference between actions

> 来源：openclaw/skills · shortcuts-skill (erik-agens)。本地缓存于 reference/。

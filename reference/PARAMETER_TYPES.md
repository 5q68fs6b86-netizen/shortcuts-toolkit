# Parameter Types Reference

Complete documentation of all parameter value types used in iOS Shortcuts.

Based on analysis of 200 real-world shortcuts containing 338 unique actions and 543 parameter keys.

---

## Serialization Types

| Serialization Type | Description | Use Case |
|--------------------|-------------|----------|
| `WFTextTokenString` | Text with embedded variable references | Text fields that can contain variables |
| `WFTextTokenAttachment` | Single variable reference | Input parameters referencing other actions |
| `WFDictionaryFieldValue` | Dictionary with key-value pairs | HTTP headers, JSON bodies |
| `WFContentPredicateTableTemplate` | Filter conditions | Find/Filter actions |
| `WFQuantityFieldValue` | Measurement with unit | Duration, file size, etc. |
| `WFContactFieldValue` | Contact field reference | Contact properties |
| `WFTimeOffsetValue` | Time offset/duration | Time adjustments |

---

## Basic Value Types

### String
```xml
<key>WFMenuPrompt</key><string>Choose an option</string>
```
### Integer
```xml
<key>WFControlFlowMode</key><integer>0</integer>
```
### Number (Float)
```xml
<key>WFNumberActionNumber</key><real>30.0</real>
```
### Boolean
```xml
<key>WFShowWorkflow</key><true/>
```
### Array
```xml
<key>WFMenuItems</key>
<array><string>Option 1</string><string>Option 2</string></array>
```
### Data (base64)
```xml
<key>WFData</key><data>BASE64_ENCODED_DATA</data>
```

---

## Variable Reference Types

### WFTextTokenAttachment (Single Variable Reference)
```xml
<key>WFInput</key>
<dict>
    <key>Value</key>
    <dict>
        <key>OutputName</key><string>Photos</string>
        <key>OutputUUID</key><string>F2BEAE11-3F38-40C3-AD1F-FD48D90F9FE2</string>
        <key>Type</key><string>ActionOutput</string>
    </dict>
    <key>WFSerializationType</key><string>WFTextTokenAttachment</string>
</dict>
```

### WFTextTokenString (Text with Variables)
- `￼` (U+FFFC) is the placeholder character
- `{0, 1}` means "at position 0, length 1"
- Multiple variables: `"Hello ￼, you have ￼ messages"` with `{6, 1}` and `{22, 1}`

---

## Dictionary Field Value (HTTP headers, JSON, form)

### WFItemType Values
| Value | Type |
|-------|------|
| 0 | Text/String |
| 1 | Number |
| 2 | Array |
| 3 | Dictionary |
| 4 | Boolean |

---

## Content Filter (WFContentPredicateTableTemplate)

Actions that use content filters:
- `filter.photos`, `filter.files`, `filter.reminders`, `filter.calendarevents`
- `filter.contacts`, `filter.notes`, `filter.music`, `filter.articles`, `filter.apps`
- `conditional` (via `WFConditions`)

See FILTERS.md.

---

## Quantity Field Value

```xml
<key>WFDuration</key>
<dict>
    <key>Value</key><dict><key>Magnitude</key><real>5.0</real><key>Unit</key><string>min</string></dict>
    <key>WFSerializationType</key><string>WFQuantityFieldValue</string>
</dict>
```

| Category | Units |
|----------|-------|
| Time | `sec`, `min`, `hr`, `days` |
| Data | `bytes`, `KB`, `MB`, `GB` |
| Length | `m`, `km`, `ft`, `mi` |

---

## Named Variable Reference
```xml
<key>WFVariable</key>
<dict>
    <key>Value</key><dict><key>Type</key><string>Variable</string><key>VariableName</key><string>myVariable</string></dict>
    <key>WFSerializationType</key><string>WFTextTokenAttachment</string>
</dict>
```

## Special Input Types

### Magic Variable (Shortcut Input)
```xml
<key>Type</key><string>ExtensionInput</string>
```
### Current Date
```xml
<key>Type</key><string>CurrentDate</string>
```
### Clipboard
```xml
<key>Type</key><string>Clipboard</string>
```

---

## App Identifier
```xml
<key>WFAppIdentifier</key><string>com.apple.safari</string>
```
Or full:
```xml
<key>WFApp</key>
<dict>
    <key>BundleIdentifier</key><string>com.apple.mobilesafari</string>
    <key>Name</key><string>Safari</string>
    <key>TeamIdentifier</key><string>0000000000</string>
</dict>
```

---

## Common Parameter Keys Across Actions

| Parameter | Count | Type | Description |
|-----------|-------|------|-------------|
| `UUID` | all | string | Action's unique identifier |
| `WFInput` | 306 | variable_ref | Input from previous action |
| `GroupingIdentifier` | ~100 | string | Links control flow actions |
| `WFControlFlowMode` | ~100 | integer | Control flow position |
| `CustomOutputName` | ~50 | string | Custom name for output |
| `WFShowWorkflow` | ~30 | boolean | Show in workflow view |

---

## Type Coercion (Aggrandizements)

### Common Coercion Classes
| Class | Description |
|-------|-------------|
| `WFStringContentItem` | Coerce to text |
| `WFNumberContentItem` | Coerce to number |
| `WFBooleanContentItem` | Coerce to boolean |
| `WFDictionaryContentItem` | Coerce to dictionary |
| `WFURLContentItem` | Coerce to URL |
| `WFImageContentItem` | Coerce to image |
| `WFFileContentItem` | Coerce to file |

### Parameter Patterns by Action Type

**Text Actions**: `WFTextActionText`, `Text` — string or WFTextTokenString
**Control Flow**: `GroupingIdentifier` (string UUID), `WFControlFlowMode` (integer)
**Input**: `WFInput` (WFTextTokenAttachment), `WFVariable` (named)
**Photos**: `WFContentItemFilter`, `photos` (DeletePhotos uses lowercase!), `WFPhotoCount`
**HTTP**: `WFURL`, `WFHTTPMethod`, `WFHTTPBodyType`, `WFHTTPHeaders`, `WFJSONValues`, `WFFormValues`

> 来源：openclaw/skills · shortcuts-skill (erik-agens)。本地缓存于 reference/。

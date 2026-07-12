# Variable Reference System

How to pass data between actions in Shortcuts.

## Overview

Shortcuts uses a UUID-based system for referencing output from previous actions:

1. **Source action** has a `UUID` parameter identifying its output
2. **Consuming action** references that UUID via `OutputUUID` in `attachmentsByRange`
3. The placeholder character `￼` (U+FFFC) marks where variables are inserted in text

## UUID Format

UUIDs must be:
- **Uppercase** letters
- Standard UUID format: `XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX`

Example: `A1B2C3D4-E5F6-7890-ABCD-EF1234567890`

---

## WFSerializationType Values

| Type | Description | Usage |
|------|-------------|-------|
| `WFTextTokenString` | Text with embedded variable references | Most common for text params |
| `WFTextTokenAttachment` | Single variable reference (no text) | When param is just a variable |
| `WFContentPredicateTableTemplate` | Filter/predicate definition | For filter actions |
| `WFDictionaryFieldValueItems` | Dictionary entries | For dictionary creation |

---

## attachmentsByRange Format

```xml
<key>attachmentsByRange</key>
<dict>
    <key>{position, length}</key>
    <dict>
        <key>OutputUUID</key>
        <string>SOURCE-ACTION-UUID</string>
        <key>OutputName</key>
        <string>Display Name</string>
        <key>Type</key>
        <string>ActionOutput</string>
    </dict>
</dict>
```

### Range Key Format

`{position, length}` where:
- **position**: Character index in the string (0-based)
- **length**: Always `1` (the placeholder is 1 character)

---

## The Placeholder Character

The Object Replacement Character `￼` (U+FFFC) serves as a placeholder in the `string` value where variables are inserted.

In XML: direct character `￼`, or escaped `&#xFFFC;` / `&#65532;`.

---

## Complete Variable Reference Structure

### WFTextTokenString (Text with Variables)

```xml
<key>ParameterName</key>
<dict>
    <key>Value</key>
    <dict>
        <key>string</key>
        <string>The result is: ￼</string>
        <key>attachmentsByRange</key>
        <dict>
            <key>{16, 1}</key>
            <dict>
                <key>OutputUUID</key>
                <string>11111111-1111-1111-1111-111111111111</string>
                <key>OutputName</key>
                <string>Result</string>
                <key>Type</key>
                <string>ActionOutput</string>
            </dict>
        </dict>
    </dict>
    <key>WFSerializationType</key>
    <string>WFTextTokenString</string>
</dict>
```

### WFTextTokenAttachment (Single Variable)

```xml
<key>ParameterName</key>
<dict>
    <key>Value</key>
    <dict>
        <key>OutputUUID</key>
        <string>11111111-1111-1111-1111-111111111111</string>
        <key>OutputName</key>
        <string>Text</string>
        <key>Type</key>
        <string>ActionOutput</string>
    </dict>
    <key>WFSerializationType</key>
    <string>WFTextTokenAttachment</string>
</dict>
```

---

## Type Values

| Type | Description |
|------|-------------|
| `ActionOutput` | Output from a previous action |
| `Variable` | Named variable (from Set Variable) |
| `CurrentDate` | Current date/time |
| `Clipboard` | Clipboard contents |
| `Ask` | Ask When Run |
| `ExtensionInput` | Shortcut input |
| `DeviceDetails` | Device information |

---

## Aggrandizements (Property Access)

### Property Access
```xml
<dict>
    <key>PropertyName</key><string>Name</string>
    <key>Type</key><string>WFPropertyVariableAggrandizement</string>
</dict>
```

### Dictionary Key Access
```xml
<dict>
    <key>DictionaryKey</key><string>keyName</string>
    <key>Type</key><string>WFDictionaryValueVariableAggrandizement</string>
</dict>
```

### Type Coercion
```xml
<dict>
    <key>CoercionItemClass</key><string>WFStringContentItem</string>
    <key>Type</key><string>WFCoercionVariableAggrandizement</string>
</dict>
```

---

## Common Output Names

| Action | OutputName |
|--------|------------|
| Text (gettext) | `Text` |
| Ask for Input | `Provided Input` |
| Ask LLM | `Response` |
| Get Weather | `Weather Conditions` |
| Get Current Location | `Current Location` |
| URL | `URL` |
| Get Contents of URL | `Contents of URL` |
| Number | `Number` |
| Date | `Date` |
| List | `List` |
| Dictionary | `Dictionary` |
| Repeat Each | `Repeat Item` |
| Repeat Count | `Repeat Index` |

> Note: Position counting includes all characters including the placeholder `￼`.
>
> 来源：openclaw/skills · shortcuts-skill (erik-agens)。本地缓存于 reference/。

# Shortcut Plist Format

Complete documentation of the `.shortcut` file structure.

## Root Structure（⚠️ 关键：扁平，WFWorkflowActions 在顶层，不要包 WFWorkflow）

A `.shortcut` file is a binary plist (can be written as XML, then converted). The root is a dictionary:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- REQUIRED -->
    <key>WFWorkflowActions</key>
    <array><!-- Array of action dictionaries --></array>

    <!-- REQUIRED - Version info -->
    <key>WFWorkflowClientVersion</key>
    <string>2700.0.4</string>
    <key>WFWorkflowClientRelease</key>
    <string>26A0000a</string>
    <key>WFWorkflowMinimumClientVersion</key>
    <integer>900</integer>
    <key>WFWorkflowMinimumClientVersionString</key>
    <string>900</string>

    <!-- REQUIRED - Icon -->
    <key>WFWorkflowIcon</key>
    <dict>
        <key>WFWorkflowIconGlyphNumber</key><integer>59511</integer>
        <key>WFWorkflowIconStartColor</key><integer>4282601983</integer>
    </dict>

    <!-- OPTIONAL -->
    <key>WFWorkflowName</key><string>My Shortcut</string>
    <key>WFWorkflowHasOutputFallback</key><false/>
    <key>WFWorkflowImportQuestions</key><array/>
    <key>WFWorkflowOutputContentItemClasses</key><array/>
    <key>WFWorkflowTypes</key><array/>
    <key>WFWorkflowInputContentItemClasses</key>
    <array>
        <string>WFStringContentItem</string>
        <string>WFURLContentItem</string>
    </array>
</dict>
</plist>
```

## Root Keys Reference

| Key | Type | Required | Description |
|-----|------|----------|-------------|
| `WFWorkflowActions` | Array | Yes | Array of action dictionaries |
| `WFWorkflowClientVersion` | String | Yes | Client version (e.g., "2700.0.4") |
| `WFWorkflowClientRelease` | String | No | Release identifier |
| `WFWorkflowMinimumClientVersion` | Integer | Yes | Minimum version (900+) |
| `WFWorkflowMinimumClientVersionString` | String | Yes | String version of minimum |
| `WFWorkflowIcon` | Dict | Yes | Icon configuration |
| `WFWorkflowName` | String | No | Display name |
| `WFWorkflowHasOutputFallback` | Boolean | No | Has output fallback |
| `WFWorkflowImportQuestions` | Array | No | Import-time questions |
| `WFWorkflowInputContentItemClasses` | Array | No | Accepted input types |
| `WFWorkflowOutputContentItemClasses` | Array | No | Output types |
| `WFWorkflowTypes` | Array | No | Workflow types |

## Icon Configuration

### Common Glyph Numbers
| Glyph | Number |
|-------|--------|
| Globe | 59511 |
| Star | 59446 |
| Heart | 59448 |
| Gear | 59458 |
| Document | 59493 |
| Folder | 59495 |
| Play | 59477 |
| Message | 59412 |

### Color Values (ARGB integers)
| Color | Value |
|-------|-------|
| Blue | 4282601983 |
| Green | 4292093695 |
| Orange | 4294967295 |
| Purple | 4285887861 |
| Gray | 2846468607 |

## Action Structure

```xml
<dict>
    <key>WFWorkflowActionIdentifier</key>
    <string>is.workflow.actions.showresult</string>
    <key>WFWorkflowActionParameters</key>
    <dict>
        <key>UUID</key><string>A1B2C3D4-E5F6-7890-ABCD-EF1234567890</string>
        <!-- ... action-specific parameters ... -->
    </dict>
</dict>
```

| Key | Type | Required | Description |
|-----|------|----------|-------------|
| `WFWorkflowActionIdentifier` | String | Yes | Action identifier |
| `WFWorkflowActionParameters` | Dict | Yes | Action configuration |

## Input Content Item Classes

`WFAppStoreAppContentItem`, `WFArticleContentItem`, `WFContactContentItem`, `WFDateContentItem`, `WFEmailAddressContentItem`, `WFGenericFileContentItem`, `WFImageContentItem`, `WFiTunesProductContentItem`, `WFLocationContentItem`, `WFDCMapsLinkContentItem`, `WFAVAssetContentItem`, `WFPDFContentItem`, `WFPhoneNumberContentItem`, `WFRichTextContentItem`, `WFSafariWebPageContentItem`, `WFStringContentItem`, `WFURLContentItem`

## Binary vs XML Plist

```bash
plutil -convert binary1 MyShortcut.shortcut   # XML → binary (optional, signing handles it)
plutil -convert xml1 MyShortcut.shortcut       # binary → XML (debugging)
```

The `shortcuts sign` command accepts both formats.

> 来源：openclaw/skills · shortcuts-skill (erik-agens)。本地缓存于 reference/。

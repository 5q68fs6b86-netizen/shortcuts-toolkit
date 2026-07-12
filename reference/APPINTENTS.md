# AppIntents Reference

Complete catalog of all 728 AppIntent actions available in macOS/iOS.

## AppIntents vs WF*Actions

| Aspect | WF*Actions | AppIntents |
|--------|-----------|------------|
| Identifier format | `is.workflow.actions.*` | Various (e.g., `OpenAboutSettingsStaticDeepLinks`) |
| Origin | Legacy Shortcuts (pre-iOS 16) | App Intents framework (iOS 16+) |
| Invocation | Direct identifier in action | Via `WFAppIntentExecutionAction` wrapper |
| Scope | Core shortcut actions | System integrations, deep links, app extensions |

## How to Invoke AppIntents

AppIntents are invoked using the `WFAppIntentExecutionAction` wrapper:

```xml
<dict>
    <key>WFWorkflowActionIdentifier</key>
    <string>is.workflow.actions.appintentexecution</string>
    <key>WFWorkflowActionParameters</key>
    <dict>
        <key>AppIntentDescriptor</key>
        <dict>
            <key>BundleIdentifier</key>
            <string>com.apple.AccessibilityUtilities.AXSettingsShortcuts</string>
            <key>Name</key>
            <string>Open VoiceOver</string>
            <key>TeamIdentifier</key>
            <string>0000000000</string>
            <key>AppIntentIdentifier</key>
            <string>OpenAccessibilityVoiceOverStaticDeepLinks</string>
        </dict>
    </dict>
</dict>
```

---

## AppIntents by Category

### Settings Deep Links (34)
`OpenAboutSettingsStaticDeepLinks`, `OpenAirDropSettingsStaticDeepLinks`, `OpenAppleIDSettingsStaticDeepLinks`, `OpenBatterySettingsStaticDeepLinks`, `OpenBluetoothSettingsStaticDeepLinks`, `OpenDisplaySettingsStaticDeepLinks`, `OpenFamilySettingsStaticDeepLinks`, `OpenFocusSettingsStaticDeepLinks`, `OpenGeneralSettingsStaticDeepLinks`, `OpenInternetAccountsSettingsStaticDeepLinks`, `OpenKeyboardSettingsStaticDeepLinks`, `OpenLanguageSettingsStaticDeepLinks`, `OpenNetworkSettingsStaticDeepLinks`, `OpenNotificationSettingsStaticDeepLinks`, `OpenPasswordsSettingsStaticDeepLinks`, `OpenPrivacySettingsStaticDeepLinks`, `OpenScreenTimeSettingsStaticDeepLinks`, `OpenSecuritySettingsStaticDeepLinks`, `OpenSiriSettingsStaticDeepLinks`, `OpenSoftwareUpdateSettingsStaticDeepLinks`, `OpenSoundSettingsStaticDeepLinks`, `OpenStorageSettingsStaticDeepLinks`, `OpenTrackpadSettingsStaticDeepLinks`, `OpenWalletSettingsStaticDeepLinks`, `OpenWiFiSettingsStaticDeepLinks`

### Accessibility (164)
Patterns: `OpenAccessibility*StaticDeepLinks`, `UpdateAx*EntityValueIntent`, `ToggleAx*`
- `OpenAccessibilityVoiceOverStaticDeepLinks`, `OpenAccessibilityZoomStaticDeepLinks`, `OpenAccessibilitySwitchControlStaticDeepLinks`
- `UpdateAxVoiceOverSpeakingRateEntityValueIntent`
- `ToggleAxVoiceOverIntent`, `ToggleAxZoomIntent`

### Clock & Alarms (23)
`CreateAlarmIntent`, `DeleteAlarmIntent`, `ToggleAlarmIntent`, `CreateTimerIntent`, `PauseTimerIntent`, `ResumeTimerIntent`, `CancelTimerIntent`, `StartStopwatchIntent`, `ResetStopwatchIntent`

### Calendar (5)
`CreateCalendarIntent`, `DeleteCalendarIntent`, `OpenCalendarScreenIntent`, `CloseCalendarScreenIntent`

### Reminders (12)
`CreateReminderListIntent`, `DeleteReminderListIntent`, `OpenReminderListIntent`, `OpenSmartReminderListIntent`, `CompleteReminderIntent`

### Notes (8)
`CreateNoteFolderIntent`, `DeleteNoteFolderIntent`, `CreateNoteTagIntent`, `DeleteNoteTagIntent`, `AddTagsToNotesIntent`, `RemoveTagsFromNotesIntent`, `PinNotesIntent`, `FindNotesIntent`

### Safari (18)
`CreateTabIntent`, `CreatePrivateTabIntent`, `CloseTabIntent`, `CreateTabGroupIntent`, `OpenTabIntent`, `OpenTabGroupIntent`, `FindBookmarksIntent`, `FindReadingListItemsIntent`, `FindTabsIntent`, `FindTabGroupsIntent`, `ChangeReaderModeStateIntent`

### Home (4)
`FindHomeIntent`, `FindHomeDeviceIntent`, `FindHomeSceneIntent`, `ToggleHomeAccessoryIntent`

### Photos (24)
`CreateMemoryIntent`, `OpenCameraIntent`, `FindPhotosIntent`, `FindAlbumsIntent`, `CreateAlbumIntent`

### Music (2)
`RecognizeMusicIntent`, `PlayMusicIntent`

### Writing Tools (3)
`ProofreadIntent`, `RewriteIntent`, `SummarizeIntent`

### Voice Memos (10)
`CreateVoiceMemoFolderIntent`, `DeleteVoiceMemoFolderIntent`, `OpenVoiceMemoFolderIntent`, `FindVoiceMemosIntent`, `PlayVoiceMemoIntent`, `DeleteVoiceMemosIntent`

### Shortcuts (8)
`CreateWorkflowIntent`, `DeleteWorkflowIntent`, `CreateiCloudLinkIntent`, `SearchShortcutsIntent`, `RunShortcutIntent`

### System Controls (154)
Patterns: `Set*ModeIntent`, `Toggle*Intent`, `Update*EntityValueIntent`, `Set*SettingIntent`
- `SetLowPowerModeIntent`, `SetAirplaneModeIntent`, `ToggleBluetoothIntent`, `SetBrightnessIntent`, `SetVolumeIntent`

### Data & Search (21)
Patterns: `Find*Intent`, `Get*Intent`, `Search*Intent`
- `FindSportsEventsIntent`, `GetPhysicalActivityIntent`, `SearchFilesIntent`

---

## Complete AppIntent Identifier List (by prefix)

### Open*
```
OpenAboutSettingsStaticDeepLinks, OpenAccessibilityAudioDescriptionsStaticDeepLinks,
OpenAccessibilityAudioStaticDeepLinks, OpenAccessibilityCaptionsStaticDeepLinks,
OpenAccessibilityDisplayStaticDeepLinks, OpenAccessibilityHearingDevicesStaticDeepLinks,
OpenAccessibilityHoverTextStaticDeepLinks, OpenAccessibilityKeyboardStaticDeepLinks,
OpenAccessibilityLiveCaptionsStaticDeepLinks, OpenAccessibilityLiveSpeechStaticDeepLinks,
OpenAccessibilityMotionStaticDeepLinks, OpenAccessibilityPersonalVoiceStaticDeepLinks,
OpenAccessibilityPointerControlStaticDeepLinks, OpenAccessibilityRootStaticDeepLinks,
OpenAccessibilityRTTStaticDeepLinks, OpenAccessibilityShortcutStaticDeepLinks,
OpenAccessibilitySiriStaticDeepLinks, OpenAccessibilitySpokenContentStaticDeepLinks,
OpenAccessibilitySwitchControlStaticDeepLinks, OpenAccessibilityVocalShortcutsStaticDeepLinks,
OpenAccessibilityVoiceControlStaticDeepLinks, OpenAccessibilityVoiceOverStaticDeepLinks,
OpenAccessibilityZoomStaticDeepLinks
```

### Create*
```
CreateAlarmIntent, CreateAlbumIntent, CreateCalendarIntent, CreateEventIntent,
CreateMemoryIntent, CreateNoteFolderIntent, CreateNoteTagIntent, CreateReminderIntent,
CreateReminderListIntent, CreateTabGroupIntent, CreateTabIntent, CreateTimerIntent,
CreateVoiceMemoFolderIntent, CreateWorkflowIntent
```

### Toggle*
```
ToggleAlarmIntent, ToggleAxAssistiveTouchIntent, ToggleAxAudioDescriptionsIntent,
ToggleAxClosedCaptioningIntent, ToggleAxColorFiltersIntent, ToggleAxFullKeyboardAccessIntent,
ToggleAxGuidedAccessIntent, ToggleAxInvertColorsIntent, ToggleAxLiveListenIntent,
ToggleAxReduceMotionIntent, ToggleAxReduceTransparencyIntent, ToggleAxSpeakScreenIntent,
ToggleAxSwitchControlIntent, ToggleAxVoiceControlIntent, ToggleAxVoiceOverIntent,
ToggleAxZoomIntent, ToggleBluetoothIntent, ToggleCellularDataIntent,
ToggleDoNotDisturbIntent, ToggleFocusModeIntent, ToggleHomeAccessoryIntent,
ToggleLowPowerModeIntent, ToggleOrientationLockIntent, ToggleWiFiIntent
```

### Set*
```
SetAirplaneModeIntent, SetAlwaysOnDisplayIntent, SetAppearanceIntent,
SetBrightnessIntent, SetCellularDataIntent, SetFlashlightIntent,
SetListeningModeIntent, SetLowPowerModeIntent, SetNightShiftIntent,
SetOrientationLockIntent, SetPersonalHotspotIntent, SetStageManagerIntent,
SetTrueToneIntent, SetVolumeIntent, SetWiFiIntent
```

### Find*
```
FindAlbumsIntent, FindBookmarksIntent, FindCalendarEventsIntent,
FindContactsIntent, FindFilesIntent, FindHomeDeviceIntent, FindHomeIntent,
FindHomeRoomIntent, FindHomeSceneIntent, FindNotesIntent, FindPhotosIntent,
FindReadingListItemsIntent, FindRemindersIntent, FindSportsEventsIntent,
FindTabGroupsIntent, FindTabsIntent, FindVoiceMemosIntent
```

---

## Common Bundle Identifiers
- `com.apple.AccessibilityUtilities.AXSettingsShortcuts` - Accessibility
- `com.apple.Preferences` - Settings
- `com.apple.clock` - Clock
- `com.apple.mobilenotes` - Notes
- `com.apple.reminders` - Reminders
- `com.apple.Safari` - Safari
- `com.apple.Home` - Home
- `com.apple.Photos` - Photos

## Invocation Template

```xml
<dict>
    <key>WFWorkflowActionIdentifier</key>
    <string>is.workflow.actions.appintentexecution</string>
    <key>WFWorkflowActionParameters</key>
    <dict>
        <key>AppIntentDescriptor</key>
        <dict>
            <key>BundleIdentifier</key><string>BUNDLE_ID</string>
            <key>Name</key><string>DISPLAY_NAME</string>
            <key>AppIntentIdentifier</key><string>APPINTENT_IDENTIFIER</string>
        </dict>
        <!-- Additional parameters as needed -->
    </dict>
</dict>
```

> 来源：openclaw/skills · shortcuts-skill (erik-agens)。本地缓存于 reference/。

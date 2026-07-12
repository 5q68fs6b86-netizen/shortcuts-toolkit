# Complete Working Examples

Copy-paste ready examples that can be signed and imported.

> 每个 `.shortcut` = `reference/PLIST_FORMAT.md` 的根 plist，内含 `WFWorkflowActions` 数组。下面只列各示例的 **action 数组**（其余根键见 PLIST_FORMAT.md / SKILL.md 的模板）。

## Example 1: Hello World

```xml
<dict>
    <key>WFWorkflowActionIdentifier</key><string>is.workflow.actions.gettext</string>
    <key>WFWorkflowActionParameters</key>
    <dict>
        <key>UUID</key><string>11111111-1111-1111-1111-111111111111</string>
        <key>WFTextActionText</key><string>Hello World!</string>
    </dict>
</dict>
<dict>
    <key>WFWorkflowActionIdentifier</key><string>is.workflow.actions.showresult</string>
    <key>WFWorkflowActionParameters</key>
    <dict>
        <key>Text</key>
        <dict>
            <key>Value</key><dict>
                <key>attachmentsByRange</key><dict>
                    <key>{0, 1}</key><dict>
                        <key>OutputName</key><string>Text</string>
                        <key>OutputUUID</key><string>11111111-1111-1111-1111-111111111111</string>
                        <key>Type</key><string>ActionOutput</string>
                    </dict>
                </dict>
                <key>string</key><string>￼</string>
            </dict>
            <key>WFSerializationType</key><string>WFTextTokenString</string>
        </dict>
    </dict>
</dict>
```

## Example 2: Ask User for Input

```xml
<dict>
    <key>WFWorkflowActionIdentifier</key><string>is.workflow.actions.ask</string>
    <key>WFWorkflowActionParameters</key>
    <dict>
        <key>UUID</key><string>AAAAAAAA-AAAA-AAAA-AAAA-AAAAAAAAAAAA</string>
        <key>WFAskActionPrompt</key><string>What is your name?</string>
        <key>WFInputType</key><string>Text</string>
    </dict>
</dict>
<dict>
    <key>WFWorkflowActionIdentifier</key><string>is.workflow.actions.showresult</string>
    <key>WFWorkflowActionParameters</key>
    <dict>
        <key>Text</key>
        <dict>
            <key>Value</key><dict>
                <key>attachmentsByRange</key><dict>
                    <key>{7, 1}</key><dict>
                        <key>OutputName</key><string>Provided Input</string>
                        <key>OutputUUID</key><string>AAAAAAAA-AAAA-AAAA-AAAA-AAAAAAAAAAAA</string>
                        <key>Type</key><string>ActionOutput</string>
                    </dict>
                </dict>
                <key>string</key><string>Hello, ￼!</string>
            </dict>
            <key>WFSerializationType</key><string>WFTextTokenString</string>
        </dict>
    </dict>
</dict>
```

## Example 3: AI Query (Ask → Apple Intelligence → Show)

```xml
<dict>
    <key>WFWorkflowActionIdentifier</key><string>is.workflow.actions.ask</string>
    <key>WFWorkflowActionParameters</key>
    <dict>
        <key>UUID</key><string>BBBBBBBB-BBBB-BBBB-BBBB-BBBBBBBBBBBB</string>
        <key>WFAskActionPrompt</key><string>What would you like to ask?</string>
        <key>WFInputType</key><string>Text</string>
    </dict>
</dict>
<dict>
    <key>WFWorkflowActionIdentifier</key><string>is.workflow.actions.askllm</string>
    <key>WFWorkflowActionParameters</key>
    <dict>
        <key>UUID</key><string>CCCCCCCC-CCCC-CCCC-CCCC-CCCCCCCCCCCC</string>
        <key>WFLLMModel</key><string>Apple Intelligence</string>
        <key>WFGenerativeResultType</key><string>Text</string>
        <key>WFLLMPrompt</key>
        <dict>
            <key>Value</key><dict>
                <key>attachmentsByRange</key><dict>
                    <key>{0, 1}</key><dict>
                        <key>OutputName</key><string>Provided Input</string>
                        <key>OutputUUID</key><string>BBBBBBBB-BBBB-BBBB-BBBB-BBBBBBBBBBBB</string>
                        <key>Type</key><string>ActionOutput</string>
                    </dict>
                </dict>
                <key>string</key><string>￼</string>
            </dict>
            <key>WFSerializationType</key><string>WFTextTokenString</string>
        </dict>
    </dict>
</dict>
<dict>
    <key>WFWorkflowActionIdentifier</key><string>is.workflow.actions.showresult</string>
    <key>WFWorkflowActionParameters</key>
    <dict>
        <key>Text</key>
        <dict>
            <key>Value</key><dict>
                <key>attachmentsByRange</key><dict>
                    <key>{0, 1}</key><dict>
                        <key>OutputName</key><string>Response</string>
                        <key>OutputUUID</key><string>CCCCCCCC-CCCC-CCCC-CCCC-CCCCCCCCCCCC</string>
                        <key>Type</key><string>ActionOutput</string>
                    </dict>
                </dict>
                <key>string</key><string>￼</string>
            </dict>
            <key>WFSerializationType</key><string>WFTextTokenString</string>
        </dict>
    </dict>
</dict>
```

## Example 4: Menu Demo (choosefrommenu)

三个 case：`Say Hello` / `Say Goodbye` / `Tell a Joke`。

- Menu Start: `WFControlFlowMode=0`, `WFMenuItems=["Say Hello","Say Goodbye","Tell a Joke"]`, `WFMenuPrompt`
- 每个 Case: `WFControlFlowMode=1`, `WFMenuItemTitle` (顺序须与 WFMenuItems 一致)
- Menu End: `WFControlFlowMode=2`
- 所有节点共享同一 `GroupingIdentifier`

（完整 XML 见 CONTROL_FLOW.md 的 Choose from Menu 模板）

## Example 5: Weather + AI Report

```xml
<!-- Get Weather -->
<dict>
    <key>WFWorkflowActionIdentifier</key><string>is.workflow.actions.weather.currentconditions</string>
    <key>WFWorkflowActionParameters</key>
    <dict><key>UUID</key><string>EEEEEEEE-EEEE-EEEE-EEEE-EEEEEEEEEEEE</string></dict>
</dict>
<!-- Build Prompt (text + weather var at pos 56) -->
<dict>
    <key>WFWorkflowActionIdentifier</key><string>is.workflow.actions.gettext</string>
    <key>WFWorkflowActionParameters</key>
    <dict>
        <key>UUID</key><string>FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF</string>
        <key>WFTextActionText</key>
        <dict>
            <key>Value</key><dict>
                <key>attachmentsByRange</key><dict>
                    <key>{56, 1}</key><dict>
                        <key>OutputName</key><string>Weather Conditions</string>
                        <key>OutputUUID</key><string>EEEEEEEE-EEEE-EEEE-EEEE-EEEEEEEEEEEE</string>
                        <key>Type</key><string>ActionOutput</string>
                    </dict>
                </dict>
                <key>string</key><string>Generate a friendly weather report based on this data:
￼

Keep it brief and include clothing recommendations.</string>
            </dict>
            <key>WFSerializationType</key><string>WFTextTokenString</string>
        </dict>
    </dict>
</dict>
<!-- Ask AI (prompt = text above) -->
<dict>
    <key>WFWorkflowActionIdentifier</key><string>is.workflow.actions.askllm</string>
    <key>WFWorkflowActionParameters</key>
    <dict>
        <key>UUID</key><string>GGGGGGGG-GGGG-GGGG-GGGG-GGGGGGGGGGGG</string>
        <key>WFLLMModel</key><string>Apple Intelligence</string>
        <key>WFGenerativeResultType</key><string>Text</key>
        <key>WFLLMPrompt</key>
        <dict>
            <key>Value</key><dict>
                <key>attachmentsByRange</key><dict>
                    <key>{0, 1}</key><dict>
                        <key>OutputName</key><string>Text</string>
                        <key>OutputUUID</key><string>FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF</string>
                        <key>Type</key><string>ActionOutput</string>
                    </dict>
                </dict>
                <key>string</key><string>￼</string>
            </dict>
            <key>WFSerializationType</key><string>WFTextTokenString</string>
        </dict>
    </dict>
</dict>
<!-- Show Result (LLM response) -->
<dict>
    <key>WFWorkflowActionIdentifier</key><string>is.workflow.actions.showresult</string>
    <key>WFWorkflowActionParameters</key>
    <dict>
        <key>Text</key>
        <dict>
            <key>Value</key><dict>
                <key>attachmentsByRange</key><dict>
                    <key>{0, 1}</key><dict>
                        <key>OutputName</key><string>Response</string>
                        <key>OutputUUID</key><string>GGGGGGGG-GGGG-GGGG-GGGG-GGGGGGGGGGGG</string>
                        <key>Type</key><string>ActionOutput</string>
                    </dict>
                </dict>
                <key>string</key><string>￼</string>
            </dict>
            <key>WFSerializationType</key><string>WFTextTokenString</string>
        </dict>
    </dict>
</dict>
```

## How to Use

1. **Copy** the action array into the root plist wrapper (PLIST_FORMAT.md)
2. **Save** as `.shortcut` (XML plist ok)
3. **Sign**: `shortcuts sign --mode anyone --input X.shortcut --output X_signed.shortcut`
4. **Import**: double-click the signed file

> 来源：openclaw/skills · shortcuts-skill (erik-agens)。本地缓存于 reference/。

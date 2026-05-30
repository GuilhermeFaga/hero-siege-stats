# PR 25 Review Findings

1. Medium: `total_guild_xp` packets are identified but still do not update XP.
   `src/engine/message_parser.py:212` routes packets with only `totalGuildXp`/`total_guild_xp` to `XPEvent`, but `src/models/events/xp.py:12` only exposes `xp_message.xp`. In `src/models/messages/xp.py:13`, `xp` becomes `0` unless a message string or gained-XP field exists, so bare renamed total-XP packets update nothing even though they are now detected.

2. Medium: field-based mail packets always report "new mail".
   `src/engine/message_parser.py:214` now treats `newMail`, `new_mail`, or `mail` fields as mail events, but `src/models/messages/mail.py:9` ignores those fields and derives state only from `message == 'No new mail'`. A packet like `{"new_mail": 0}` or `{"newMail": false}` will incorrectly set `new_mail = 1`.

3. Low/Medium: account alias detection is not backed by account alias parsing.
   `src/engine/message_parser.py:220` can identify account packets using aliases like `class_id` or `heroLevel`, but `src/models/messages/account.py:97-101` still requires original keys like `name`, `class`, and `herolevel`. Those packets will be caught and dropped in `message_to_event`, so account/season mode updates can silently fail.

## Testing

No tests were run locally during review. GitHub reported no PR checks for this branch.

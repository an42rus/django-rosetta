from django import dispatch
entry_changed = dispatch.Signal(
    providing_args=["user", "old_msgstr", "old_fuzzy", "pofile", "language_code",]
)

post_save = dispatch.Signal(
    providing_args=["language_code","request",]
)

reload_server = dispatch.Signal(
    providing_args=["request", ]
)

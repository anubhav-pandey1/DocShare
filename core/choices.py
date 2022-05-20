class AccessLevelChoices:

    UNAUTHORIZED = 1
    VIEWER = 10
    EDITOR = 50
    OWNER = 100

    LIST = [
        (UNAUTHORIZED, "Unauthorized"),
        (VIEWER, "Viewer"),
        (EDITOR, "Editor"),
        (OWNER, "Owner"),
    ]

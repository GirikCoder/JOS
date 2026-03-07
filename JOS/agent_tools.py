JARVIS_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "create_item",
            "description": "Creates a file or folder in a safe zone (Desktop, Documents, or Downloads). Default is Desktop if no destination is provided.",
            "parameters": {
                "type": "object",
                "properties": {
                    "item_name": {
                        "type": "string",
                        "description": "The name of the file or folder to create. If it contains 'folder' or 'directory', a folder is created. Otherwise, a text file is created."
                    },
                    "destination": {
                        "type": "string",
                        "description": "The destination folder. Allowed values: 'desktop', 'documents', 'downloads'."
                    }
                },
                "required": ["item_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_item",
            "description": "Deletes a file or folder from a safe zone.",
            "parameters": {
                "type": "object",
                "properties": {
                    "item_name": {
                        "type": "string",
                        "description": "The name of the file or folder to delete."
                    }
                },
                "required": ["item_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "system_control",
            "description": "Controls system hardware settings such as volume and screen brightness.",
            "parameters": {
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string",
                        "description": "The target to control. Allowed values: 'volume', 'brightness'."
                    },
                    "action": {
                        "type": "string",
                        "description": "The action to perform. Examples: 'mute', 'unmute', 'increase', 'decrease', or a specific number spanning 0-100 indicating the level."
                    }
                },
                "required": ["target", "action"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "open_app",
            "description": "Opens an application on the user's computer.",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {
                        "type": "string",
                        "description": "The name of the application to open. Examples: 'chrome', 'calculator'."
                    }
                },
                "required": ["app_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "close_app",
            "description": "Closes a running application on the user's computer.",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {
                        "type": "string",
                        "description": "The name of the application to close."
                    }
                },
                "required": ["app_name"]
            }
        }
    }
]

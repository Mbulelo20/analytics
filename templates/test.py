import os
import json
if not os.path.exists("bulkdata.json"):
        # If the file does not exist, create it and write default data (if provided)
        with open("bulkdata.json", 'w') as json_file:
            if "bulkdata.json" is not None:
                json.dump({"name": "mbulelo", "data":"hey"}, json_file, indent=4)
            else:
                # If no default data provided, create an empty JSON object
                json.dump({}, json_file, indent=4)
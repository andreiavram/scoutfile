class Component:
    symmetrical = True
    source_to_target = {
        "descriptor": "face parte din",
        "relationship": "part_of"
    }

    target_to_source = {
        "descriptor": "are în componență",
        "relationship": "has_part"
    }


class Storage:
    symmetrical = True
    source_to_target = {
        "descriptor": "este înmagazinat în",
        "relationship": "stored_in"
    }
    target_to_source = {
        "descriptor": "este container pentru",
        "relationship": "stores"
    }


class Tool:
    symmetrical = True
    source_to_target = {
        "descriptor": "este necesar pentru mentenanța",
        "relationship": "tool_for"
    }
    target_to_source = {
        "descriptor": "are nevoie pentru mentenanță de",
        "relationship":  "needs_tool"
    }



INVENTORY_RELATIONSHIPS = [Component, Storage, Tool]
INVENTORY_RELATIONSHIPS_CHOICES = list()

for rel in INVENTORY_RELATIONSHIPS:
    INVENTORY_RELATIONSHIPS_CHOICES += [(rel.source_to_target.get("relationship"), rel.source_to_target.get("descriptor")), ]
    INVENTORY_RELATIONSHIPS_CHOICES += [(rel.target_to_source.get("relationship"), rel.target_to_source.get("descriptor")), ]

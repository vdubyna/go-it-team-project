from fields.tag import Tag


class BaseEntity:
    def __init__(self) -> None:
        self.tags: list[Tag] = []

    def add_tags(self, tags: list[str]) -> None:
        self_tags = getattr(self, "tags", [])
        for tag in set(tags):
            if tag not in [tag.value for tag in self_tags]:
                self_tags.append(Tag(tag))
        self.tags = self_tags

    def remove_tags(self, tags: list[str]) -> None:
        self_tags = getattr(self, "tags", [])
        filtered = []
        for tag in self_tags:
            if tag.value not in tags:
                filtered.append(tag)
        self.tags = filtered
    
    def includes_tag(self, tag: str) -> bool:
        return any(t.value == tag for t in getattr(self, "tags", []))
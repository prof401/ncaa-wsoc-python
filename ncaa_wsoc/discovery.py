"""DiscoveryManager: queue for newly discovered team IDs."""

from collections import deque


class DiscoveryManager:
    """
    Tracks known team IDs and a queue of teams to scrape.
    When an opponent is found that isn't in known_ids, add to queue.
    """

    def __init__(self, known_ids: set[str] | None = None):
        """
        Args:
            known_ids: Initial set of team IDs already known (from seed + existing CSV).
        """
        self._known: set[str] = set(known_ids or ())
        self._queue: deque[tuple[str, str | None]] = deque()

    def add_if_new(self, team_id: str, name_hint: str | None = None) -> bool:
        """
        Add team_id to the discovery queue if not already known.

        Args:
            team_id: NCAA team ID.
            name_hint: Optional display name from the link text (e.g. schedule opponent).

        Returns:
            True if newly added to queue, False if already known.
        """
        if not team_id:
            return False
        if team_id in self._known:
            return False
        self._known.add(team_id)
        hint = name_hint.strip() if name_hint else None
        self._queue.append((team_id, hint or None))
        return True

    def add_seed_ids(self, entries: list[tuple[str, str | None]]) -> None:
        """
        Add seed team IDs to the queue (all are "new" for processing).
        Marks them as known so they won't be re-added from opponent discovery.

        Args:
            entries: (team_id, display_name) pairs from the rankings seed.
        """
        for tid, name_hint in entries:
            tid = (tid or "").strip()
            if not tid or tid in self._known:
                continue
            self._known.add(tid)
            hint = name_hint.strip() if name_hint else None
            self._queue.append((tid, hint or None))

    def pop_next(self) -> tuple[str, str | None] | None:
        """
        Pop the next queued team.

        Returns:
            (team_id, name_hint) where name_hint may be None, or None if empty.
        """
        if not self._queue:
            return None
        return self._queue.popleft()

    def is_empty(self) -> bool:
        """Return True if the queue has no more teams to process."""
        return len(self._queue) == 0

    def __len__(self) -> int:
        """Number of teams remaining in the queue."""
        return len(self._queue)

import re

from .exceptions import InvalidOperation


class Tracker:
    REGEX = r"(?P<name>[a-z]+)(?P<number>[0-9]+)"

    def __init__(self):
        self.hosts = {}

    def allocate(self, hostname):
        if hostname not in self.hosts:
            self.hosts[hostname] = {1, }
            return self._format_server_name(hostname, 1)
        else:
            server_number = self._next_server_number(hostname)
            self.hosts[hostname].add(server_number)
            return self._format_server_name(hostname, server_number)

    def deallocate(self, server_name):
        hostname, server_number = self._parse_server_name(server_name)
        try:
            self.hosts[hostname].remove(server_number)
        except (AttributeError, KeyError):
            raise InvalidOperation()

    def _parse_server_name(self, server_name):
        if m := re.search(Tracker.REGEX, server_name):
            return m.group("name"), int(m.group("number"))
        else:
            raise InvalidOperation()

    def _next_server_number(self, hostname):
        return min(
            set(
                range(1, max(self.hosts[hostname]) + 2)
            ).difference(self.hosts[hostname])
        )

    def _format_server_name(self, hostname, server_number):
        return f"{hostname}{server_number}"


class NoSilentTracker(Tracker):
    def allocate(self, hostname):
        try:
            return super().allocate(hostname)
        except Exception as e:
            return str(e)

    def deallocate(self, server_name):
        try:
            return super().deallocate(server_name)
        except Exception as e:
            return str(e)


class SilentTracker(Tracker):
    def allocate(self, hostname):
        try:
            return super().allocate(hostname)
        except Exception:
            return None

    def deallocate(self, server_name):
        try:
            super().deallocate(server_name)
        except Exception:
            return None

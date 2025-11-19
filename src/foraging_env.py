"""
foraging_env.py
----------------
A small foraging environment for hub-based routing experiments...

The idea:
- Start at a chosen hub.
- Have a limited travel budget in km.
- Visit customers one by one.
- Reward = their importance score (w_importance).
- Cost = distance travelled.

This is intentionally simple ,,, just enough to compare policies like:
    * nearest neighbour
    * greedy importance
    * importance / distance ratio
"""

import numpy as np
from src.geo_utils import haversine_km


class ForagingEnv:
    """
    Minimal environment for hub routing simulations.
    """

    def __init__(self, df_customers, df_hubs, hub_id, distance_col, budget_km=400.0):
        # Filter customers belonging to this hub
        self.customers = df_customers[df_customers["assigned_hub"] == hub_id].copy()
        self.customers = self.customers.reset_index(drop=True)

        # Hub coordinates
        hub_row = df_hubs[df_hubs["HUB_ID"] == hub_id].iloc[0]
        self.hub_lat = hub_row["LATTUD"]
        self.hub_lon = hub_row["LNGTUD"]

        self.distance_col = distance_col
        self.budget_km = float(budget_km)

        # initialize state
        self.reset()

    # -------------------------------------------------------

    def reset(self):
        """Reset environment state before running a tour."""
        self.current_lat = self.hub_lat
        self.current_lon = self.hub_lon
        self.remaining_km = self.budget_km
        self.total_reward = 0.0
        self.total_distance = 0.0

        # nothing is visited initially
        self.customers["visited"] = False

        # to store visited sequence
        self.path = []
        return self._get_obs()

    # -------------------------------------------------------

    def _get_obs(self):
        """Return a small state snapshot (for logs)."""
        return {
            "current_lat": self.current_lat,
            "current_lon": self.current_lon,
            "remaining_km": self.remaining_km,
            "total_reward": self.total_reward,
            "total_distance": self.total_distance,
        }

    # -------------------------------------------------------

    def step(self, idx):
        """
        Visit the customer at index `idx`.
        Returns: (obs, reward, done, info)
        """

        # avoid visiting twice
        if self.customers.loc[idx, "visited"]:
            return self._get_obs(), 0.0, False, {"msg": "already visited"}

        # target coordinates
        row = self.customers.loc[idx]
        lat = row["LATTUD"]
        lon = row["LNGTUD"]

        # distance from current position
        travel_km = haversine_km(self.current_lat, self.current_lon, lat, lon)

        if travel_km > self.remaining_km:
            # nope — cannot reach
            return self._get_obs(), 0.0, True, {"msg": "budget exhausted"}

        # move
        self.current_lat = lat
        self.current_lon = lon
        self.remaining_km -= travel_km
        self.total_distance += travel_km

        # importance reward
        reward = row["w_importance"]
        self.total_reward += reward

        # mark visited
        self.customers.loc[idx, "visited"] = True
        self.path.append(idx)

        # check if done
        unvisited = self.customers[~self.customers["visited"]]
        done = len(unvisited) == 0

        return self._get_obs(), reward, done, {"travel_km": travel_km, "msg": "ok"}


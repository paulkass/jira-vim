
import json
import jira
from jira import JIRA
from ..common.scrumBoard import ScrumBoard

class ObjectNode:
    def __init__(self, obj, parent, *children):
        self.obj = obj
        self.parent = parent
        self.children = children if children else []

    def add_child(self, child):
        self.children.append(child)

    def is_leaf(self):
        return not self.children

    def find_items_at_depth(self, predicate=lambda o: True, depth=float("inf")):
        """
        Find items that satisfy certain conditions

        Takes a predicate function, and examines all items using depth first search with depth exactly "depth" and gives them to the predicate. If the predicate returns True, adds the item to the return list. Returns the full list.

        Parameters
        ----------
        predicate : Function (Optional)
            The predicate function. Accepts one parameter, the object (not the node itself), and returns either True or False. If returns True, the item is included in the return list. Defaults to a True predicate.
        depth : Integer (Optional)
            The specified depth. If an integer, only nodes at that depth can be returned. If the depth is Infinity, examines all leaf nodes. Defaults to Infinity
        """
        if not depth or (self.is_leaf() and depth == float("inf")):
            return [self] if predicate(self.obj) else []

        return_list = []
        for c in self.children:
            return_list.extend(c.find_items_at_depth(predicate=predicate, depth=depth-1))
        return return_list

class ObjectStorageTrie:
    """
    This class is designed to store objects in a Trie structure. Here are the depth specifications:
        Depth 0: Root Node.
        Depth 1: Projects
        Depth 2: Boards
        Depth 3: Sprints
    """

    def __init__(self, jiraObj):
        """
        Initialize an object storage trie from a JIRA object

        Initialize a tree by populating all the depths of the trie with objects obtained from the JIRA interface. Projects are native JIRA objects while Boards and Sprints are custom objects defined in python.common

        Parameters
        ----------
        jiraObj : a JIRA Object
            A JIRA object that is used to browse the structure of the jiraObj instance.

        Returns
        -------
        Nothing
        """
        self.jira = jiraObj
        self.root = ObjectNode("root", None)

        projects = self.jira.projects()
        for p in projects:
            objNode = ObjectNode(p, self.root)
            self.root.add_child(objNode)

        boards = self.jira.boards()
        for b in boards:
            project_id = str(b.location.projectId)
            project_key = str(b.location.projectKey)
            project_predicate = lambda o, p_id=project_id, p_key=project_key: str(o.id) == p_id and str(o.key) == p_key
            results = self.root.find_items_at_depth(project_predicate, depth=1)
            assert len(results) == 1

            proj_node = results[0]
            board_node = ObjectNode(b, proj_node)
            proj_node.add_child(board_node)

            if isinstance(b, ScrumBoard):
                sprints = self.jira.sprints(b.id)
                for s in sprints:
                    sprint_node = ObjectNode(s, board_node)
                    board_node.add_child(sprint_node)

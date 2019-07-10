
import json
import jira
from jira import JIRA
import math

class ObjectNode:
    def __init__(self, obj, parent, *children):
        self.obj = obj
        self.parent = parent
        self.children = children if children else []

    def add_child(self, child):
        self.children.append(child)

    def find_items(self, predicate, depth=float("inf")):
        if not depth:
            return [self] if predicate(self) else []
        


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
            print(b.name)

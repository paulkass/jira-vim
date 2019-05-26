
class ItemCategorizer():
    def issueCategorizer(self, issues, statusToColumn, columnToIssues):
        for i in issues:
            key = (i["key"], i["fields"]["summary"])
            statusId = i["fields"]["status"]["id"]
            column = statusToColumn[statusId]
            if column not in columnToIssues:
                columnToIssues[column] = set()
            columnToIssues[column].add(key)

        return [(a, list(b)) for a, b in columnToIssues.items() if len(b) > 0]
        

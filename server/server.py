from flask import Flask, jsonify, request, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory storage
groups = [
    {
        "id": 1,
        "groupName": "Group 1",
        "members": [1, 2, 3],
    },
    {
        "id": 2,
        "groupName": "Group 2",
        "members": [4, 5],
    },
]

students = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"},
    {"id": 4, "name": "David"},
    {"id": 5, "name": "Eve"},
]

@app.route('/api/groups', methods=['GET'])
def get_groups():
    """
    Route to get all groups
    return: Array of group objects
    """
    return jsonify(groups)

@app.route('/api/students', methods=['GET'])
def get_students():
    """
    Route to get all students
    return: Array of student objects
    """
    return jsonify(students)

@app.route('/api/groups', methods=['POST'])
def create_group():
    """
    Route to add a new group
    param groupName: The name of the group (from request body)
    param members: Array of member names (from request body)
    return: The created group object
    """
    
    # Getting the request body (DO NOT MODIFY)
    group_data = request.json
    group_name = group_data.get("groupName")
    group_members = group_data.get("members")
    
    # edge case: check if the group name is empty
    if not group_name:
        abort(400, "Group name is required")   
    # edge case: check if the group members is empty
    if not group_members:
        abort(400, "Group members are required")
    # edge case: check if group name is overlapping
    if any(group_name == group["groupName"] for group in groups):
        abort(400, "Group name already exists")
    
    # Create a new group with an incremented ID
    new_id = max(group["id"] for group in groups) + 1 if groups else 1
    # convert the group members to string, for example ['loll'] to 'loll' 
    group_members = str(group_members)
    # remove the brackets from the string, for example 'loll' to loll
    group_members = group_members[1:-1]
    # print(group_members)
    # remove the quotes from the string, for example 'loll' to loll
    group_members = group_members.replace("'", "")
    member_names = group_members.split(',')
    
    # print(member_names[0])
    group_members = []
    # loop over ['fewfew', 'a', 'b', 'd', 'f'] by index
    for i in range(len(member_names)):
        name = member_names[i].strip()
        # edge case: check if the member name is alpabetic
        if not name.isalpha():
            print(name)
            abort(400, "Invalid member name")
        # print(name)
        # Create a new student with incremented ID
        new_student_id = len(students) + 1
        new_student = {"id": new_student_id, "name": name}
        students.append(new_student)
        group_members.append(new_student_id)
    
    # print(group_members)
    new_group = {
        "id": new_id,
        "groupName": group_name,
        "members": group_members
    }
    
    # Add the new group to our groups list
    groups.append(new_group)
    # print(groups)
    # print(students)
    return jsonify(new_group), 201

@app.route('/api/groups/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    """
    Route to delete a group by ID
    param group_id: The ID of the group to delete
    return: Empty response with status code 204
    """
    global groups
    
    # Find the group with the specified ID
    group_index = next((i for i, group in enumerate(groups) if group["id"] == group_id), None)
    
    # If the group exists, remove it
    if group_index is not None:
        groups.pop(group_index)
    else:
        abort(404, "Group not found")

    return '', 204  # Return 204 (do not modify this line)

@app.route('/api/groups/<int:group_id>', methods=['GET'])
def get_group(group_id):
    """
    Route to get a group by ID (for fetching group members)
    param group_id: The ID of the group to retrieve
    return: The group object with member details
    """
    # Find the group with the specified ID
    group = next((g for g in groups if g["id"] == group_id), None)
    
    if group:
        # Get detailed member information for this group
        member_details = []
        for member_id in group["members"]:
            student = next((s for s in students if s["id"] == member_id), None)
            if student:
                member_details.append(student)
        
        # Return the group with detailed member information
        return jsonify({
            "id": group["id"],
            "groupName": group["groupName"],
            "members": member_details
        })
    else:
        abort(404, "Group not found")

if __name__ == '__main__':
    app.run(port=3902, debug=True)

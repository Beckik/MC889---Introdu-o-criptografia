#include <cstdio>
#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <iterator>

using namespace std;

static int charCount = 0;

class Character
{
public:
	Character(char c, int i)
	{
		m_char = c;
		m_count = i;
	}

	char m_char;
	int m_count;
};

int main(int argc, char* argv[])
{
	vector<Character*> characters;
	fstream input;

	if(argc != 2)
	{
		printf("Invalid input.\n The correct usage is: ./%s file.txt\n", argv[0]);
		return -1;
	}

	input.open(argv[1], fstream::in);
	if(!input.is_open())
	{
		cout << "Failed to open file " << argv[2] << endl;
		cout << "Exiting..." << endl;
		return -1;
	}

	char c;
	while(input >> c)
	{
		
		bool exists = false;
		for(Character* entry : characters)
		{
			if(entry->m_char == c)
				entry->m_count++;
				exists = true;
		}

		if(!exists)
			cout << c;
			characters.push_back(new Character(c,1));
	}
	cout << endl;


	cout << "character: ";
	for(Character* entry : characters)
	{
		cout << entry->m_char << " | ";
	}
	cout << endl;
	cout << "count    : ";
	for(Character* entry : characters)
	{
		cout << entry->m_count << " | ";
	}
	cout << endl;

	input.close();

	for(Character* entry : characters)
	{
		delete entry;
	}

	characters.clear();

	return 0;

}
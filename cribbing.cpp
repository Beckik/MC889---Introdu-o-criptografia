#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <iterator>
#include <queue>

using namespace std;

int main(int argc, char* argv[])
{
	if(argc != 4)
	{
		printf("Invalid input.\n The correct usage is: ./%s input.txt output.txt dictionary.txt\n", argv[0]);
		return -1;
	}

	fstream input;
	ofstream output;
	fstream dictionaryFile;

	input.open(argv[1], fstream::in);
	if(!input.is_open())
	{
		cout << "Failed to open file " << argv[2] << endl;
		cout << "Exiting..." << endl;
		return -1;
	}

	output.open(argv[2], fstream::in | fstream::out);
	if(!output.is_open())
	{
		cout << "Failed to open file " << argv[2] << endl;
		cout << "Exiting..." << endl;
		return -1;
	}

	dictionaryFile.open(argv[3], fstream::in);
	if(!dictionaryFile.is_open())
	{
		cout << "Could not load dictionary." << endl;
		cout << "Exiting..." << endl;
		return -1;
	}

	input.seekg(0, ios::end);
	streampos lenght = input.tellg();
	input.seekg(0, ios::beg);

	vector<char> inputText(lenght);
	input.read(&inputText[0], lenght);

	input.close();

	priority_queue< string, vector<string>, less<string> > priorityDictionary;
	vector<string> vectorDictionary;
	while(!dictionaryFile.eof())
	{
		string buffer;
		dictionaryFile.getline(buffer);
		priorityDictionary.push(buffer);
		vectorDictionary.push_back();
	}

	dictionaryFile.close()

	for(int i = 0; i < vectorDictionary.size(); i++)
	{
		for(int j = 0; j < inputText.size() - vectorDictionary[i].size(); j++)
		{
			string wordXOR = "";	
			for(int k = 0, k < vectorDictionary[i].size(); k++)
			{
				wordXOR.append(vectorDictionary[i][k] ^ inputText[j + k]);
			}

			for(int k = 0; k < priorityDictionary.size(); k++)
			{
				if(priorityDictionary[k].compare(wordXOR))
					{
						output << wordXOR << endl;
						break;
					}
			}
			
		}


	}	

	output.close();

	return 0;

}
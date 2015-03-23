#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <iterator>

using namespace std;

int main(int argc, char* argv[])
{
	if(argc != 3)
	{
		printf("Invalid input.\n The correct usage is: ./%s input.txt output.txt\n", argv[0]);
		return -1;
	}

	fstream input;
	fstream output;

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

	input.seekg(0, ios::end);
	streampos lenght = input.tellg();
	input.seekg(0, ios::beg);

	vector<char> inputText(lenght);
	input.read(&inputText[0], lenght);

	cout << "Enter the word: ";
	string word;
	getline(cin, word);

	cout << inputText.size() << endl;

	for(int i = 0; i < inputText.size() - 5; i++)
	{
		for(int j = 0; j < word.size(); j++)
		{
			output.put(word[j] ^ inputText[i + j]);
		}
		output << endl;
	}

	input.close();
	output.close();

	return 0;

}
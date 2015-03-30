#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <iterator>
#include <queue>
#include <map>
#include <string.h>
#include <regex>
#include <streambuf>
#include <sstream>
#include <cstddef>

using namespace std;

vector<string> sxor(string ctext, string crib);
void printResults(string text);

struct split
{
	enum empties_t { empties_ok, no_empties };
};

template <typename Container>
Container& split(
	Container&                            result,
	const typename Container::value_type& s,
	const typename Container::value_type& delimiters,
	split::empties_t                      empties = split::empties_ok)
{
	result.clear();
	size_t current;
	size_t next = -1;
	do
	{
		if (empties == split::no_empties)
		{
			next = s.find_first_not_of(delimiters, next + 1);
			if (next == Container::value_type::npos) break;
			next -= 1;
		}
		current = next + 1;
		next = s.find_first_of(delimiters, current);
		result.push_back(s.substr(current, next - current));
	} while (next != Container::value_type::npos);
	return result;
}

int main(int argc, char* argv[])
{
	if (argc != 2)
	{
		printf("Invalid input.\n The correct usage is: ./%s input.txt output.txt dictionary.txt\n", argv[0]);
		return -1;
	}

	fstream input;
	//ofstream output;
	fstream dictionaryFile;
	
	cout << argv[1] << endl;

	input.open(argv[1], fstream::in | fstream::binary);
	if (!input.is_open())
	{
		cout << "Failed to open file " << argv[1] << endl;
		cout << "Exiting..." << endl;
		return -1;
	}

	/*
	output.open(argv[2], fstream::in | fstream::out);
	if (!output.is_open())
	{
		cout << "Failed to open file " << argv[2] << endl;
		cout << "Exiting..." << endl;
		return -1;
	}
	*/

	dictionaryFile.open(argv[3], fstream::in);
	if (!dictionaryFile.is_open())
	{
		cout << "Could not load dictionary." << endl;
		cout << "Exiting..." << endl;
		return -1;
	} 
	
	input.seekg(0, input.end);
	int lenght = input.tellg();
	input.seekg(0, input.beg);

	char* buf = new char[lenght];
	string cipher;
	
	for (int i = 0; i < lenght; i++)
	{
		input.get(buf[i]);
		cipher += buf[i];
	}

	delete buf;

	input.close();

	vector<string> dictionary;
	while (!dictionaryFile.eof())
	{
		string line;
		getline(dictionaryFile, line);
		dictionary.push_back(line);
	}

	dictionaryFile.close();

	string plainText1(cipher.size(), '_');
	string plainText2(cipher.size(), '_');

	regex charset("^[a-zA-Z0-9.,?! :;\']+$");

	string option;
	string crib;

	while (option.compare("end"))
	{


		cout << "Plaintext 1:" << endl;
		printResults(plainText1);
		cout << "Plaintext 2:" << endl;
		printResults(plainText2);

		cout << "Enter the crib: ";
		getline(cin, crib);

		vector<string> results;
		results = sxor(cipher, crib);

		for (int i = 0; i < results.size(); i++)
		{
			if (results[i].size() != crib.size())
				break;
			if (regex_search(results[i], charset))
				cout << i << ": " << results[i] << endl;
		}

		cout << "Enter the position, 'none' for no match or 'end' to end: ";
		getline(cin, option);

		try
		{
			int pos = stoi(option);
			if (pos < 0 || pos > cipher.size())
				throw;
			
			int textNumber = 0;
			while (textNumber < 1 || textNumber > 2)
			{
				cout << "Is this part of the text 1 or text 2? (1/2): ";
				getline(cin, option);

				textNumber = stoi(option);

				if (textNumber == 1)
				{
					plainText1.replace(pos, crib.size(), crib);
					plainText2.replace(pos, results[pos].size(), results[pos]);
				}
				else if (textNumber == 2)
				{
					plainText2.replace(pos, crib.size(), crib);
					plainText1.replace(pos, results[pos].size(), results[pos]);
				}
				else
				{
					cout << "Invalid option. Try again." << endl;
				}
			}
		}
		catch (...)
		{
			if (!option.compare("end"))
			{
				cout << "The plaintext 1 is: " << plainText1 << endl;
				cout << "The plaintext 2 is: " << plainText2 << endl;
			}
			else if (!option.compare("none"))
			{
				cout << "No changes made." << endl;
			}
			else
			{
				cout << "Invalid entry." << endl;
			}
		}
	}
}

vector<string> sxor(string ctext, string crib)
{
	vector<string> results;
	string single_result;

	for (int i = 0; i < ctext.size() - crib.size(); i++)
	{
		single_result.clear();
		for (int j = 0; j < crib.size(); j++)
		{
			char temp = ctext[i + j] ^ crib[j];
			single_result += temp;
		}
		results.push_back(single_result);
	}

	return results;
}

void printResults(string text)
{
	int line_width = 40;
	
	for (int i = 0; i < text.size(); i += line_width)
	{
		if (i > text.size() - line_width)
		{
			cout << i << ": " << text.substr(i, text.size() - i) << endl;
		}
		else 
			cout << i << ": " << text.substr(i, line_width) << endl;
	}
}

void useDictionary(vector<string> dictionary, string cipher, string & plaintext1, string & plaintext2, regex charset)
{
	for (int i = 0; i < dictionary.size(); i++)
	{
		vector<string> results;
		results = sxor(cipher, dictionary[i]);

		map<int, string> goodResult;

		for (int j = 0; j < results.size(); j++)
		{
			if (results[j].size() != dictionary[i].size())
				break;
			if (regex_search(results[i], charset))
				goodResult[j] = results[j];
		}

		for (map<int, string>::iterator it = goodResult.begin(); it != goodResult.end(); it++)
		{
			for (int j = 0; j < dictionary.size(); i++)
			{
				if (dictionary[j].find(it->second))
				{

				}
			}
		}


	}

	
}


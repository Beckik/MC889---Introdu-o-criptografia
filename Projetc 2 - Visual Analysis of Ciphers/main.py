from PIL import Image
import time
import argparse
import affine
import tea

def  main(): 
    parser = argparse.ArgumentParser(description='Image encriprition tool Uses the affine cipher or the Tiny Encryption Algorithm. Can also display ppm images for convenience.')
    parser.add_argument('image', help='Path to PPM image to be processed.')
    parser.add_argument('output', help='Output path to the result.')
    parser.add_argument('-e', '--encrypt', action="count", help='Set to encription mode.')
    parser.add_argument('-d', '--decrypt', action="count", help='Set to decription mode.')
    parser.add_argument('--cipher', required=True, type=str, choices=['affine', 'tea', 'none'], default='none', help='''Sets the cipher to be used by the program. If 'none' is chosen, the specified image will be displayed. Defaults to 'none'.''')
    args = parser.parse_args()

    if(args.encrypt == 0 and args.decrypt == 0 and args.cipher != 'none'):
        print('You have to either set decrypt or encrypt on to run the script.')
        parser.print_help()
        return
    elif(args.encrypt == 0 and args.decrypt == 0):
        print("You can't set both modes on.")
        parser.print_help()
        return

 
    image = Image.open(args.image)

    imData = image.getdata()

    if(args.cipher != 'none'):
        pixelData = []
        for pixel in list(imData):
            pixelData.append(list(pixel))

        result = []

    if args.cipher == 'affine':
        ''' Affine cipher call '''
        if(args.encrypt):
            print('Insert keys "a" and "b", respectively.')
            keyA = int(input('Key "a": '))
            keyB = int(input('Key "b": '))
            if not affine.checkKeys(keyA, keyB):
                print('Invalid keys, try again.')
                keyA = int(input('Key "a": '))
                keyB = int(input('Key "b": '))

            print('Starting encription...')
            result = affine.encrypt(pixelData, keyA, keyB)
            print('Encription successfull.')
        elif(args.decrypt):
            print('Insert keys "a" and "b", respectively.')
            keyA = int(input('Key "a": '))
            keyB = int(input('Key "b": '))
            if not affine.checkKeys(keyA, keyB):
                print('Invalid keys, try again.')
                keyA = int(input('Key "a": '))
                keyB = int(input('Key "b": '))

            print('Starting decription...')
            result = affine.decrypt(pixelData, keyA, keyB)
            print('Decription successfull.')

    elif args.cipher == 'tea':
        '''TEA cipher call'''

        key = []

        print('Insert the four parts of the key in hexadecimal (32 bits, e.g.: 0x943abc12).')
        for i in range(4):
            keypart = input("Part [" + str(i) + "]: 0x" )
            try:
                decimal = int(keypart, 16)
                key.append(decimal)
            except:
                print('Invalid value, try again.')
                i = i - 1

        mode = input("Enter the mode of operation ('ecb'/'cfb'): ")


        if(args.encrypt):      
            print('Starting encription...')
            if(mode == 'ecb'):
                result = tea.encrypt_ECB(pixelData, key)
            elif(mode == 'cfb'):
                result = tea.encrypt_CFB(pixelData, key)
            print('Encription successfull.')

        elif(args.decrypt):
            print('Starting decription...')
            if(mode == 'ecb'):
                result = tea.decrypt_ECB(pixelData, key)
            elif(mode == 'cfb'):
                result = tea.decrypt_CFB(pixelData, key)
            print('Decription successfull.')

    elif args.cipher == 'none':
        '''Just shows image and exits'''
        image.show()
        return

    #print(str(result))

    print('Saving image as ' + args.output + '...')
    resultImage = Image.new(image.mode, image.size)
    resultImage.putdata(result)
    resultImage.show()

    if(args.encrypt):
        resultImage.save(args.output)
    elif(args.decrypt):
        resultImage.save(args.output)
    
    print('Image saved as ' + args.output + '...')
    return

if __name__ == '__main__':
    main()



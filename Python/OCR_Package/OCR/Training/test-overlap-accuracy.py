from TracedDigitsDataset import TracedDigitsDataset
from OCR.OkraDigitCounter import OkraDigitCounter, TransposeImage, FlattenImage
import torchvision.transforms as transforms
import torch
from pathlib import Path
from termcolor import colored


test_old_method = True
test_model_in_training_folder = False
test_model_in_weights_folder = True


# Transformations to be applied to the images
transform = transforms.Compose([
    transforms.ConvertImageDtype(torch.float32),
    transforms.Normalize(0.0, 1.0),
    FlattenImage(),
    TransposeImage()
])


def main():

    data_folder = Path(__file__).parent / 'data' / 'TracedDigits'

    data = TracedDigitsDataset(data_folder)

    print()

    if test_old_method:
        print(colored('Testing with old method', color='blue', attrs=['bold']))
        run_test(data, model_to_test='none')

    if test_model_in_training_folder:
        print(colored('Testing with ML model (Training folder weights)', color='blue', attrs=['bold']))
        run_test(data, model_to_test='train')

    if test_model_in_weights_folder:
        print(colored('Testing with ML model (Weights folder weights)', color='blue', attrs=['bold']))
        run_test(data, model_to_test='current')


def run_test(data, model_to_test):

    correct_1 = 0
    correct_2 = 0
    correct_3 = 0

    total_1 = 0
    total_2 = 0
    total_3 = 0

    if model_to_test == 'train':
        model = prepare_model(True)

    elif model_to_test == 'current':
        model = prepare_model(False)

    for segment, label in data:

        label = int(label) + 1

        if model_to_test == 'none':
            guess = get_digit_count(segment)

        else:
            guess = get_digit_count_model(segment, model)


        if guess == label:
            if label == 1:
                correct_1 += 1
                total_1 += 1

            elif label == 2:
                correct_2 += 1
                total_2 += 1

            else:
                correct_3 += 1
                total_3 += 1

        elif label == 1:
            total_1 += 1

        elif label == 2:
            total_2 += 1

        else:
            total_3 += 1

    num_correct = correct_1 + correct_2 + correct_3
    accuracy = 100 * num_correct / len(data)

    print()
    print('1 digit:', correct_1, 'of', total_1)
    print('2 digit:', correct_2, 'of', total_2)
    print('3 digit:', correct_3, 'of', total_3)
    print()
    print('Total:', num_correct, 'of', len(data))
    print(colored(f'Accuracy: {accuracy:>0.2f}%', attrs=['underline']))
    print()


def get_digit_count(img):

    height = img.shape[1]
    width = img.shape[2]

    two_digit_factor = 1.4
    three_digit_factor = 2.0

    if width >= three_digit_factor * height:

        return 3

    elif width >= two_digit_factor * height:

        return 2

    else:
        return 1


def get_digit_count_model(img, model):

    img = transform(img)
    img = img.unsqueeze(dim=0)

    prediction = model(img)
    prediction = torch.nn.functional.softmax(prediction, dim=1)

    return torch.argmax(prediction, dim=1) + 1


def prepare_model(use_training_weights):

    model = OkraDigitCounter()
    model.to(torch.device('cpu'))

    if use_training_weights:
        weights_file = Path(__file__).parent / 'okra-counter.pt'
    else:
        weights_file = Path(__file__).parent.parent / 'weights' / 'okra-counter.pt'

    state_dict = torch.load(
        weights_file,
        weights_only=True,
        map_location=torch.device('cpu')
    )
    model.load_state_dict(state_dict)

    return model


if __name__ == '__main__':
    main()
